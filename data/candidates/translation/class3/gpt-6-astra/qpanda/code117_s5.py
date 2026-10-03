# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def decompose_unitary(unitary):
    matrix = np.asarray(unitary, dtype=complex)
    if matrix.shape != (4, 4):
        raise ValueError("unitary must be a 4x4 matrix")
    if not np.allclose(matrix.conj().T @ matrix, np.eye(4), atol=1e-10):
        raise ValueError("The input matrix must be unitary")

    native_decomposer = getattr(pq, "matrix_decompose", None)
    if native_decomposer is not None:
        try:
            return native_decomposer([0, 1], matrix)
        except TypeError:
            try:
                return native_decomposer(matrix, [0, 1])
            except TypeError:
                pass

    circuit = pq.QCircuit()

    def append(gate):
        nonlocal circuit
        circuit << gate

    def phase(qubit, angle):
        append(pq.U3(qubit, 0.0, 0.0, float(angle)))

    def controlled_su2(control, target, rotation):
        theta = 2.0 * np.arctan2(
            abs(rotation[1, 0]), abs(rotation[0, 0])
        )
        p = np.angle(rotation[0, 0])
        q = np.angle(rotation[1, 0])
        alpha = float(q - p)
        gamma = float(-q - p)
        theta = float(theta)

        append(pq.RZ(target, (gamma - alpha) / 2.0))
        append(pq.CNOT(control, target))
        append(pq.RZ(target, -(alpha + gamma) / 2.0))
        append(pq.RY(target, -theta / 2.0))
        append(pq.CNOT(control, target))
        append(pq.RY(target, theta / 2.0))
        append(pq.RZ(target, alpha))

    reduced = matrix.copy()
    rotations = []
    for column in range(3):
        for row in range(3, column, -1):
            upper = row - 1
            a = reduced[upper, column]
            b = reduced[row, column]
            norm = np.hypot(abs(a), abs(b))
            if norm == 0.0:
                continue
            rotation = np.array(
                [[a.conjugate(), b.conjugate()], [-b, a]],
                dtype=complex,
            ) / norm
            reduced[[upper, row], :] = (
                rotation @ reduced[[upper, row], :]
            )
            rotations.append((upper, row, rotation.conj().T))

    angles = np.angle(np.diag(reduced))
    global_phase = float(angles[0])
    append(pq.RZ(0, -2.0 * global_phase))
    phase(0, 2.0 * global_phase)
    phase(0, angles[1] - angles[0])
    phase(1, angles[2] - angles[0])

    conditional_phase = float(
        angles[3] - angles[2] - angles[1] + angles[0]
    )
    phase(0, conditional_phase / 2.0)
    phase(1, conditional_phase / 2.0)
    append(pq.CNOT(1, 0))
    phase(0, -conditional_phase / 2.0)
    append(pq.CNOT(1, 0))

    for upper, lower, rotation in reversed(rotations):
        if (upper, lower) == (0, 1):
            append(pq.X(1))
            controlled_su2(1, 0, rotation)
            append(pq.X(1))
        elif (upper, lower) == (2, 3):
            controlled_su2(1, 0, rotation)
        else:
            append(pq.CNOT(0, 1))
            controlled_su2(1, 0, rotation[::-1, ::-1])
            append(pq.CNOT(0, 1))

    return circuit
