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
        raise ValueError("unitary must be a 4x4 matrix")
    if not np.allclose(matrix.conj().T @ matrix, np.eye(4)):
        raise ValueError("unitary must be unitary")

    circuit = pq.matrix_decompose(qubits, matrix)
    program = pq.QProg()
    program << circuit
    decomposed = pq.transform_to_base_qgate(
        program, machine, ["U3"], ["CNOT"]
    )
    if decomposed is not None:
        program = decomposed
    if isinstance(program, pq.QCircuit):
        return program
    return pq.cast_qprog_qcircuit(program)


atexit.register(lambda: machine.finalize())
