# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, RX, RZ, CNOT
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    # Qiskit Pauli string: leftmost char is qubit n-1, rightmost is qubit 0.
    # Reverse so that index i corresponds to qubit i.
    pauli_string = pauli_string[::-1]
    
    circuit = QCircuit()
    
    non_id = []
    for i, char in enumerate(pauli_string):
        if char != 'I':
            non_id.append((i, char))
    
    if not non_id:
        return circuit
    
    # Basis change before
    for qubit, char in non_id:
        if char == 'X':
            circuit << H(qubit)
        elif char == 'Y':
            circuit << RX(qubit, np.pi / 2)
    
    # CNOT chain
    target = non_id[-1][0]
    for qubit, _ in non_id[:-1]:
        circuit << CNOT(qubit, target)
    
    # Apply RZ(2*time) on target
    circuit << RZ(target, 2 * time)
    
    # Uncompute CNOT chain
    for qubit, _ in reversed(non_id[:-1]):
        circuit << CNOT(qubit, target)
    
    # Basis change after (inverse)
    for qubit, char in non_id:
        if char == 'X':
            circuit << H(qubit)
        elif char == 'Y':
            circuit << RX(qubit, -np.pi / 2)
    
    return circuit
