# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    rev_str = pauli_string[::-1]
    
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    pauli_map = {'I': I, 'X': X, 'Y': Y, 'Z': Z}
    
    P = pauli_map[rev_str[0]]
    for char in rev_str[1:]:
        P = np.kron(P, pauli_map[char])
    
    dim = 2 ** n
    U = np.cos(time) * np.eye(dim, dtype=complex) - 1j * np.sin(time) * P
    
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit(cirq.MatrixGate(U).on(*qubits))
    return circuit
