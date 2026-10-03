# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, Qubit, H, RX, RZ, CNOT

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qc = QCircuit(n)
    qubits = [Qubit(i) for i in range(n)]
    
    # Apply basis changes before Z evolution
    for i, p in enumerate(pauli_string):
        if p == 'X':
            qc << H(qubits[i])
        elif p == 'Y':
            qc << RX(np.pi/2, qubits[i])
    
    # Find non-identity qubits
    non_id = [i for i, p in enumerate(pauli_string) if p != 'I']
    
    if len(non_id) > 0:
        # CNOT chain
        for i in range(len(non_id)-1):
            qc << CNOT(qubits[non_id[i]], qubits[non_id[i+1]])
        
        # RZ on last qubit
        qc << RZ(2 * time, qubits[non_id[-1]])
        
        # Reverse CNOT chain
        for i in reversed(range(len(non_id)-1)):
            qc << CNOT(qubits[non_id[i]], qubits[non_id[i+1]])
    
    # Undo basis changes after Z evolution
    for i in reversed(range(n)):
        p = pauli_string[i]
        if p == 'X':
            qc << H(qubits[i])
        elif p == 'Y':
            qc << RX(-np.pi/2, qubits[i])
    
    return qc
