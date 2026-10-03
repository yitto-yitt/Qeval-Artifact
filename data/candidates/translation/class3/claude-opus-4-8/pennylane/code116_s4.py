# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np
from scipy.linalg import expm


def synthesize_evolution_gate(pauli_string, time):
    paulis = {
        'I': np.array([[1, 0], [0, 1]], dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex),
    }

    P = np.array([[1.0]], dtype=complex)
    for c in pauli_string:
        P = np.kron(P, paulis[c])

    U = expm(-1j * time * P)
    n = len(pauli_string)

    dev = qml.device('default.qubit', wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.QubitUnitary(U, wires=range(n))
        return qml.state()

    return circuit
