# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    for pauli_str, t in zip(pauli_strings, times):
        # Basis changes to map Pauli to Z
        for i, p in enumerate(pauli_str):
            if p == 'X':
                circuit.append(cirq.H(qubits[i]))
            elif p == 'Y':
                circuit.append(cirq.S**-1(qubits[i]))
                circuit.append(cirq.H(qubits[i]))
            elif p in ('Z', 'I'):
                pass
            else:
                raise ValueError(f"Invalid Pauli character: {p}")
        # Z rotation block
        if n > 1:
            for i in range(n - 1):
                circuit.append(cirq.CNOT(qubits[i], qubits[i+1]))
        circuit.append(cirq.rz(2 * t).on(qubits[-1]))
        if n > 1:
            for i in reversed(range(n - 1)):
                circuit.append(cirq.CNOT(qubits[i], qubits[i+1]))
        # Inverse basis changes
        for i in reversed(range(n)):
            p = pauli_str[i]
            if p == 'X':
                circuit.append(cirq.H(qubits[i]))
            elif p == 'Y':
                circuit.append(cirq.H(qubits[i]))
                circuit.append(cirq.S(qubits[i]))
            elif p in ('Z', 'I'):
                pass
    return circuit
