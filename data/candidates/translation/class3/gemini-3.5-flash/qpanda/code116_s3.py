# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import *
import math

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAllocMany(n)
    
    circ = QCircuit()
    
    reversed_string = pauli_string[::-1]
    active_qubits = []
    for i, char in enumerate(reversed_string):
        if char != 'I':
            active_qubits.append((i, char))
            
    if not active_qubits:
        return circ
        
    # Step 1: Basis change to Z
    for i, char in active_qubits:
        if char == 'X':
            circ << H(q[i])
        elif char == 'Y':
            circ << RX(q[i], math.pi / 2)
            
    # Step 2: CNOT staircase
    for k in range(len(active_qubits) - 1):
        circ << CNOT(q[active_qubits[k][0]], q[active_qubits[k+1][0]])
        
    # Step 3: RZ evolution
    last_qubit_idx = active_qubits[-1][0]
    circ << RZ(q[last_qubit_idx], 2 * time)
    
    # Step 4: Reverse CNOT staircase
    for k in range(len(active_qubits) - 2, -1, -1):
        circ << CNOT(q[active_qubits[k][0]], q[active_qubits[k+1][0]])
        
    # Step 5: Reverse basis change
    for i, char in active_qubits:
        if char == 'X':
            circ << H(q[i])
        elif char == 'Y':
            circ << RX(q[i], -math.pi / 2)
            
    return circ
