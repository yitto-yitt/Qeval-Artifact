# EVAL_META: task_id=41, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def compose_op():
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    I = np.eye(2, dtype=complex)
    
    # Qiskit's Pauli("YX") applies X to qubit 0 and Y to qubit 1 of the Pauli operator.
    # qargs=[0, 2] maps Pauli qubit 0 to system qubit 0, and Pauli qubit 1 to system qubit 2.
    # In Qiskit's little-endian matrix representation, qubit 2 is the most significant (leftmost in kron).
    op_matrix = np.kron(Y, np.kron(I, X))
    return op_matrix

machine.finalize()
