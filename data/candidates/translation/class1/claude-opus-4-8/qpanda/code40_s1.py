# EVAL_META: task_id=40, framework=qpanda, class=1
import numpy as np
from pyqpanda3.core import QCircuit, QProg, CPUQVM, measure

def init_random_3qubit(desired_vector):
    vec = np.asarray(desired_vector, dtype=complex)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm

    n = 3

    def build_state_circuit(amplitudes, qubits):
        circ = QCircuit()
        amps = list(amplitudes)
        num = len(qubits)

        def recurse(level, amp_list, available_qubits):
            if len(amp_list) <= 1:
                return
            half = len(amp_list) // 2
            zero_part = amp_list[:half]
            one_part = amp_list[half:]

            p0 = sum(abs(a) ** 2 for a in zero_part)
            p1 = sum(abs(a) ** 2 for a in one_part)
            total = p0 + p1

            target = available_qubits[0]
            rest = available_qubits[1:]

            if total < 1e-15:
                return

            theta = 2 * np.arctan2(np.sqrt(p1), np.sqrt(p0))

            from pyqpanda3.core import RY, RZ

            circ << RY(target, theta)

            phase0 = 0.0
            phase1 = 0.0
            if p0 > 1e-15:
                phase0 = np.angle(sum(zero_part))
            if p1 > 1e-15:
                phase1 = np.angle(sum(one_part))

            recurse(level + 1, zero_part, rest)
            recurse(level + 1, one_part, rest)

        # Simple amplitude encoding via full decomposition fallback:
        return circ

    # Use a robust state preparation: decompose with controlled rotations
    from pyqpanda3.core import RY, RZ, X

    circ = QCircuit()

    # General multiplexed initialization (disentangling, mirror of Qiskit initialize)
    def disentangle(amplitudes):
        # returns list of (gate_type, qubit, angle, controls)
        ops = []
        cur = list(amplitudes)
        for k in range(n):
            # qubit being disentangled is qubit k (LSB first in Qiskit ordering)
            new_len = len(cur) // 2
            new_amps = [0j] * new_len
            ry_angles = []
            rz_angles = []
            for i in range(new_len):
                a = cur[2 * i]
                b = cur[2 * i + 1]
                r = np.sqrt(abs(a) ** 2 + abs(b) ** 2)
                if r < 1e-15:
                    theta = 0.0
                    phi = 0.0
                    mag = 0.0
                else:
                    theta = 2 * np.arctan2(abs(b), abs(a))
                    ang_a = np.angle(a)
                    ang_b = np.angle(b)
                    phi = ang_b - ang_a
                    mag = r
                ry_angles.append(theta)
                rz_angles.append(phi)
                avg_phase = (np.angle(a) + np.angle(b)) / 2 if r >= 1e-15 else 0.0
                new_amps[i] = mag * np.exp(1j * avg_phase)
            ops.append((k, ry_angles, rz_angles))
            cur = new_amps
        return ops

    ops = disentangle(list(vec))

    # Build inverse circuit (initialize = inverse of disentangle)
    # Disentangle uniformly controlled gates; we apply the inverse in reverse.
    def apply_ucry(target, controls, angles, sign):
        # uniformly controlled RY over `controls` (list of qubit indices)
        m = len(controls)
        for idx in range(2 ** m):
            # apply X on controls where bit is 0
            flips = []
            for j in range(m):
                if not ((idx >> j) & 1):
                    flips.append(controls[j])
            for q in flips:
                circ << X(q)
            ang = sign * angles[idx]
            if abs(ang) > 1e-15:
                if m == 0:
                    circ << RY(target, ang)
                else:
                    g = RY(target, ang)
                    circ << g.control(controls)
            for q in flips:
                circ << X(q)

    def apply_ucrz(target, controls, angles, sign):
        m = len(controls)
        for idx in range(2 ** m):
            flips = []
            for j in range(m):
                if not ((idx >> j) & 1):
                    flips.append(controls[j])
            for q in flips:
                circ << X(q)
            ang = sign * angles[idx]
            if abs(ang) > 1e-15:
                if m == 0:
                    circ << RZ(target, ang)
                else:
                    g = RZ(target, ang)
                    circ << g.control(controls)
            for q in flips:
                circ << X(q)

    # initialize = reverse(disentangle) with negated angles
    for k in reversed(range(n)):
        target = k
        controls = list(range(k + 1, n))
        _, ry_angles, rz_angles = ops[k]
        apply_ucrz(target, controls, rz_angles, +1)
        apply_ucry(target, controls, ry_angles, -1)

    prog = QProg()
    prog << circ
    prog << measure(0, 0)
    prog << measure(1, 1)
    prog << measure(2, 2)

    qvm = CPUQVM()
    qvm.run(prog, 100000)
    counts = qvm.result().get_counts()

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
