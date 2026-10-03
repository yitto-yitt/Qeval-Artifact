# EVAL_META: task_id=117, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def decompose_unitary(unitary):
    matrix = np.asarray(unitary, dtype=np.complex128)
    if matrix.shape != (4, 4):
        raise ValueError("unitary must be a 4x4 matrix.")
    if not np.allclose(matrix.conj().T @ matrix, np.eye(4)):
        raise ValueError("The supplied matrix is not unitary.")

    probe = pq.QProg()
    probe << pq.X(qubits[0]) << pq.I(qubits[1])
    probe_matrix = np.asarray(pq.get_matrix(probe)).reshape(4, 4)
    little_endian = np.allclose(
        probe_matrix,
        np.kron(np.eye(2), np.array([[0, 1], [1, 0]])),
    )
    permutation = [0, 2, 1, 3]

    for synthesis_matrix in (
        matrix,
        matrix[np.ix_(permutation, permutation)],
    ):
        program = pq.QProg()
        program << pq.matrix_decompose(qubits, synthesis_matrix)
        reconstructed = np.asarray(pq.get_matrix(program)).reshape(4, 4)
        if not little_endian:
            reconstructed = reconstructed[np.ix_(permutation, permutation)]

        overlap = np.vdot(matrix, reconstructed) / 4.0
        if abs(overlap) > 0 and np.allclose(
            reconstructed,
            (overlap / abs(overlap)) * matrix,
            atol=1e-8,
            rtol=1e-8,
        ):
            break
    else:
        raise RuntimeError("The synthesized circuit does not reproduce the unitary.")

    pq.transform_to_base_qgate(program, machine, ["U3"], ["CNOT"])
    return pq.cast_qprog_qcircuit(program)


atexit.register(lambda: machine.finalize())
