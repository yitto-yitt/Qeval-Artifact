# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n_qubits = len(pauli_string)
    qubits = [cirq.LineQubit(i) for i in range(n_qubits)]
    
    # Convert Pauli string to Cirq Pauli term
    pauli_term = cirq.PauliString()
    for i, pauli_char in enumerate(pauli_string):
        if pauli_char == 'X':
            pauli_term *= cirq.X(qubits[i])
        elif pauli_char == 'Y':
            pauli_term *= cirq.Y(qubits[i])
        elif pauli_char == 'Z':
            pauli_term *= cirq.Z(qubits[i])
        # 'I' is identity, so we skip it (multiply by 1)
    
    # Create the evolution circuit using exponentiation
    circuit = cirq.Circuit(cirq.PauliStringPhasor(pauli_term, exponent=-time).on(*qubits))
    
    return circuit
