# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, RY, RZ, H, CNOT, SWAP


def initialize_adjoint_and_compose(data1, data2):
    def read_choi(data):
        raw = data if isinstance(data, (np.ndarray, list, tuple)) else data.data
        matrix = np.asarray(raw, dtype=complex)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("A Choi matrix must be square.")
        if callable(getattr(data, "input_dims", None)):
            din = int(np.prod(data.input_dims()))
            dout = int(np.prod(data.output_dims()))
        else:
            din = int(np.sqrt(matrix.shape[0]))
            dout = din
        if din < 1 or dout < 1 or din * dout != matrix.shape[0]:
            raise ValueError("Cannot infer valid channel dimensions.")
        return matrix, din, dout

    def pack(matrix, din, dout):
        mi = max(1, (din - 1).bit_length())
        mo = max(1, (dout - 1).bit_length())
        tensor = np.zeros((1 << mi, 1 << mo, 1 << mi, 1 << mo), complex)
        tensor[:din, :dout, :din, :dout] = matrix.reshape(din, dout, din, dout)
        return tensor.ravel(), mi, mo

    def multiplex(prog, rotation, target, controls, angles):
        angles = np.asarray(angles, dtype=float).copy()
        count = len(angles)
        step = 1
        while step < count:
            for start in range(0, count, 2 * step):
                left = angles[start:start + step].copy()
                right = angles[start + step:start + 2 * step].copy()
                angles[start:start + step] = left + right
                angles[start + step:start + 2 * step] = left - right
            step *= 2
        angles /= count
        for k in range(count):
            gray = k ^ (k >> 1)
            prog << rotation(target, float(angles[gray]))
            if controls:
                following = (k + 1) % count
                next_gray = following ^ (following >> 1)
                bit = (gray ^ next_gray).bit_length() - 1
                prog << CNOT(controls[-1 - bit], target)

    def prepare(prog, vector, offset):
        norm = float(np.linalg.norm(vector))
        amplitudes = vector / norm if norm else np.zeros_like(vector)
        if not norm:
            amplitudes[0] = 1
        n = (len(amplitudes) - 1).bit_length()
        wires = list(range(offset + n - 1, offset - 1, -1))
        weights = np.abs(amplitudes) ** 2
        phases = np.angle(amplitudes)

        for depth, target in enumerate(wires):
            blocks = weights.reshape(1 << depth, 2, -1).sum(axis=2)
            angles = 2 * np.arctan2(np.sqrt(blocks[:, 1]), np.sqrt(blocks[:, 0]))
            multiplex(prog, RY, target, wires[:depth], angles)

        for depth, target in enumerate(wires):
            means = phases.reshape(1 << depth, 2, -1).mean(axis=2)
            multiplex(prog, RZ, target, wires[:depth], means[:, 1] - means[:, 0])

        return norm * np.exp(1j * float(phases.mean()))

    def simulate(prog, nqubits):
        machine = CPUQVM()
        try:
            result = machine.run(prog)
        except TypeError:
            result = machine.run(prog, 1)

        expected = 1 << nqubits
        objects = [machine, result]
        visited = set()
        state_names = (
            "get_state_vector", "get_qstate", "get_q_state",
            "get_state", "state_vector", "qstate",
        )
        for obj in objects:
            if obj is None or id(obj) in visited:
                continue
            visited.add(id(obj))
            candidates = []
            if isinstance(obj, (np.ndarray, list, tuple)):
                candidates.append(obj)
            for name in state_names:
                accessor = getattr(obj, name, None)
                if accessor is None:
                    continue
                try:
                    candidates.append(accessor() if callable(accessor) else accessor)
                except (TypeError, RuntimeError):
                    continue
            for candidate in candidates:
                try:
                    state = np.asarray(candidate, dtype=complex).reshape(-1)
                except (TypeError, ValueError):
                    continue
                if state.size == expected:
                    return state
            for name in ("result", "get_result"):
                accessor = getattr(obj, name, None)
                if accessor is not None:
                    try:
                        objects.append(accessor() if callable(accessor) else accessor)
                    except (TypeError, RuntimeError):
                        pass
        raise RuntimeError("The simulator did not expose its state vector.")

    matrix1, din1, dout1 = read_choi(data1)
    matrix2, din2, dout2 = read_choi(data2)
    if dout1 != din2:
        raise ValueError("Channel dimensions do not permit composition.")

    vector1, mi1, mo1 = pack(matrix1, din1, dout1)
    vector2, mi2, mo2 = pack(matrix2, din2, dout2)
    n1 = 2 * (mi1 + mo1)
    n2 = 2 * (mi2 + mo2)

    original_program = QProg()
    original_scale = prepare(original_program, vector1, 0)
    original_state = simulate(original_program, n1) * original_scale
    choi1 = original_state.reshape(
        1 << mi1, 1 << mo1, 1 << mi1, 1 << mo1
    )[:din1, :dout1, :din1, :dout1].reshape(matrix1.shape).copy()

    adjoint_program = QProg()
    adjoint_scale = prepare(adjoint_program, vector1.conj(), 0)
    groups = (
        list(range(n1 - 1, mi1 + 2 * mo1 - 1, -1)),
        list(range(mi1 + 2 * mo1 - 1, mi1 + mo1 - 1, -1)),
        list(range(mi1 + mo1 - 1, mo1 - 1, -1)),
        list(range(mo1 - 1, -1, -1)),
    )
    desired = groups[1] + groups[0] + groups[3] + groups[2]
    locations = list(range(n1))
    for destination, source in zip(range(n1 - 1, -1, -1), desired):
        current = locations.index(source)
        if current != destination:
            adjoint_program << SWAP(current, destination)
            locations[current], locations[destination] = (
                locations[destination], locations[current]
            )
    adjoint_state = simulate(adjoint_program, n1) * adjoint_scale
    adjoint_choi1 = adjoint_state.reshape(
        1 << mo1, 1 << mi1, 1 << mo1, 1 << mi1
    )[:dout1, :din1, :dout1, :din1].reshape(matrix1.shape).copy()

    composition_program = QProg()
    scale1 = prepare(composition_program, vector1, 0)
    scale2 = prepare(composition_program, vector2, n1)
    for bit in range(mo1):
        output_row = mi1 + mo1 + bit
        input_row = n1 + mi2 + 2 * mo2 + bit
        output_column = bit
        input_column = n1 + mo2 + bit
        composition_program << CNOT(output_row, input_row) << H(output_row)
        composition_program << CNOT(output_column, input_column) << H(output_column)

    composition_state = simulate(composition_program, n1 + n2)
    i, c, j, e = np.indices((din1, dout2, din1, dout2), dtype=np.int64)
    indices = (
        (i << (mi1 + 2 * mo1))
        | (j << mo1)
        | (c << (n1 + mi2 + mo2))
        | (e << n1)
    )
    composed_choi = (
        composition_state[indices] * scale1 * scale2 * (1 << mo1)
    ).reshape(din1 * dout2, din1 * dout2)

    return choi1, adjoint_choi1, composed_choi
