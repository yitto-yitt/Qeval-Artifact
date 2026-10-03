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

    mat = np.array([[1.0 + 0j]])
    for ch in pauli_string:
        mat = np.kron(mat, paulis[ch])

    unitary = expm(-1j * time * mat)

    num_qubits = len(pauli_string)
    wires = list(range(num_qubits))

    ops = [qml.QubitUnitary(unitary, wires=wires)]
    tape = qml.tape.QuantumScript(ops)
    return tape
