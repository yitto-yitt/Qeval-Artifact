# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H, RX, RZ, CNOT
import math

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = [Qubit(i) for i in range(n)]
    circuit = QCircuit()
    for pauli_str, t in zip(pauli_strings, times):
        # Reverse the string to match Qiskit's little-endian convention
        reversed_pauli = pauli_str[::-1]
        active = [i for i, p in enumerate(reversed_pauli) if p != 'I']
        if not active:
            continue
        # Basis changes
        for i in active:
            p = reversed_pauli[i]
            if p == 'X':
                circuit << H(qubits[i])
            elif p == 'Y':
                circuit << RX(qubits[i], math.pi / 2)
            # Z: no basis change
        # CNOT chain
        for i in range(len(active) - 1):
            circuit << CNOT(qubits[active[i]], qubits[active[i+1]])
        # Rotation
        circuit << RZ(qubits[active[-1]], 2 * t)
        # Inverse CNOT chain
        for i in reversed(range(len(active) - 1)):
            circuit << CNOT(qubits[active[i]], qubits[active[i+1]])
        # Inverse basis changes
        for i in reversed(active):
            p = reversed_pauli[i]
            if p == 'X':
                circuit << H(qubits[i])
            elif p == 'Y':
                circuit << RX(qubits[i], -math.pi / 2)
    return circuit
