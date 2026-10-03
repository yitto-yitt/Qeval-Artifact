# EVAL_META: task_id=112, framework=cirq, class=3
import numpy as np
import cirq

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()
    
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    pauli_map = {'I': I, 'X': X, 'Y': Y, 'Z': Z}
    
    for pauli_string, time in zip(pauli_strings, times):
        mat = np.array([[1]], dtype=complex)
        for p in pauli_string:
            mat = np.kron(mat, pauli_map[p])
            
        for _ in range(reps):
            t_rep = time / reps
            U = np.cos(t_rep) * np.eye(2**n_qubits, dtype=complex) - 1j * np.sin(t_rep) * mat
            gate = cirq.MatrixGate(U)
            circuit.append(gate.on(*qubits))
            
    return circuit
