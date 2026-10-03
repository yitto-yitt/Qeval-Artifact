# EVAL_META: task_id=112, framework=qpanda, class=3
import math
from pyqpanda3.core import QCircuit, QubitAllocator, H, RX, RZ, CNOT

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    allocator = QubitAllocator()
    qubits = allocator.allocate(num_qubits)
    circuit = QCircuit()

    for pauli_string, time in zip(pauli_strings, times):
        non_identity_indices = [i for i, p in enumerate(pauli_string) if p != 'I']
        if not non_identity_indices:
            continue

        for i, p in enumerate(pauli_string):
            if p == 'X':
                circuit << H(qubits[i])
            elif p == 'Y':
                circuit << RX(qubits[i], math.pi / 2.0)

        for control, target in zip(non_identity_indices, non_identity_indices[1:]):
            circuit << CNOT(qubits[control], qubits[target])

        circuit << RZ(qubits[non_identity_indices[-1]], 2.0 * time)

        for control, target in reversed(list(zip(non_identity_indices, non_identity_indices[1:]))):
            circuit << CNOT(qubits[control], qubits[target])

        for i, p in enumerate(pauli_string):
            if p == 'X':
                circuit << H(qubits[i])
            elif p == 'Y':
                circuit << RX(qubits[i], -math.pi / 2.0)

    return circuit
