# EVAL_META: task_id=117, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
atexit.register(lambda: machine.finalize())


def decompose_unitary(unitary):
    matrix = np.asarray(
        unitary.data if hasattr(unitary, "data") else unitary,
        dtype=np.complex128,
    )
    if matrix.shape != (4, 4):
        raise ValueError("unitary must be a 4x4 matrix")
    if not np.allclose(matrix.conj().T @ matrix, np.eye(4)):
        raise ValueError("The input matrix must be unitary")

    for positive_sequence in (False, True):
        circuit = pq.matrix_decompose(qubits, matrix, positive_sequence)
        program = pq.QProg()
        program << circuit
        actual = np.asarray(pq.get_matrix(program), dtype=complex).reshape(4, 4)
        overlap = np.vdot(matrix, actual)
        if abs(overlap) > 0 and np.allclose(
            actual, matrix * overlap / abs(overlap), atol=1e-8
        ):
            break
    else:
        raise RuntimeError("Unitary decomposition failed verification")

    program = pq.transform_to_base_qgate(
        program, machine, ["U3"], ["CNOT"]
    )
    return pq.cast_qprog_qcircuit(program)
