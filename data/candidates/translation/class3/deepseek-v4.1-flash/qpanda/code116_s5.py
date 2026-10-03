# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, Qubit, H, RZ, CNOT

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    circuit = QCircuit()
    qubits = [Qubit(i) for i in range(n)]
    
    active_indices = []
    for i, char in enumerate(pauli_string):
        if char == 'X':
            circuit << H(qubits[i])
            active_indices.append(i)
        elif char == 'Y':
            circuit << RZ(qubits[i], -np.pi/2)
            circuit << H(qubits[i])
            active_indices.append(i)
        elif char == 'Z':
            active_indices.append(i)
        # 'I' does nothing
    
    if not active_indices:
        return circuit
    
    target = active_indices[-1]
    others = active_indices[:-1]
    
    for idx in others:
        circuit << CNOT(qubits[idx], qubits[target])
    
    circuit << RZ(qubits[target], 2 * time)
    
    for idx in reversed(others):
        circuit << CNOT(qubits[idx], qubits[target])
    
    for i in active_indices:
        char = pauli_string[i]
        if char == 'X':
            circuit << H(qubits[i])
        elif char == 'Y':
            circuit << H(qubits[i])
            circuit << RZ(qubits[i], np.pi/2)
        # 'Z' does nothing
    
    return circuit
