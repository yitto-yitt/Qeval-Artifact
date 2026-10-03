# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np
import cirq

def compose_op():
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    I = np.eye(2, dtype=complex)
    
    # Qiskit's Pauli("YX") applies X to qubit 0 and Y to qubit 1 of the Pauli operator.
    # Mapping with qargs=[0, 2] places X on qubit 0 and Y on qubit 2 of the 3-qubit system.
    # Qiskit's tensor product order is Q2 (x) Q1 (x) Q0.
    return np.kron(Y, np.kron(I, X))
