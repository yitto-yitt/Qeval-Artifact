# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    machine = CPUQVM()
    try:
        machine.init_qvm()
    except AttributeError:
        machine.initQVM()
        
    n_qubits = len(pauli_string)
    try:
        qubits = machine.qAlloc_many(n_qubits)
    except AttributeError:
        qubits = machine.qAllocMany(n_qubits)
        
    circuit = QCircuit()
    
    # Find active qubits (non-I)
    active_qubits = []
    for i in range(n_qubits):
        op = pauli_string[n_qubits - 1 - i]
        if op != 'I':
            active_qubits.append(i)
            
    if not active_qubits:
        circuit._machine = machine
        return circuit
        
    # 1. Basis change to Z
    for q in active_qubits:
        op = pauli_string[n_qubits - 1 - q]
        if op == 'X':
            circuit << H(qubits[q])
        elif op == 'Y':
            circuit << RX(qubits[q], np.pi / 2)
            
    # 2. CNOT chain
    k = len(active_qubits)
    for j in range(k - 1):
        circuit << CNOT(qubits[active_qubits[j]], qubits[active_qubits[j+1]])
        
    # 3. RZ rotation
    target_q = active_qubits[-1]
    circuit << RZ(qubits[target_q], 2 * time)
    
    # 4. Inverse CNOT chain
    for j in range(k - 2, -1, -1):
        circuit << CNOT(qubits[active_qubits[j]], qubits[active_qubits[j+1]])
        
    # 5. Inverse basis change
    for q in active_qubits:
        op = pauli_string[n_qubits - 1 - q]
        if op == 'X':
            circuit << H(qubits[q])
        elif op == 'Y':
            circuit << RX(qubits[q], -np.pi / 2)
            
    circuit._machine = machine
    return circuit
