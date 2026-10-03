# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, RX, CNOT, RZ
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qc = QCircuit()
    for i in range(n):
        qc << RZ(i, 0.0)
    
    non_i = [i for i, p in enumerate(pauli_string) if p != 'I']
    if not non_i:
        return qc
    
    target = non_i[-1]
    
    for i in non_i:
        p = pauli_string[i]
        if p == 'X':
            qc << H(i)
        elif p == 'Y':
            qc << RX(i, np.pi / 2)
    
    for i in non_i:
        if i != target:
            qc << CNOT(i, target)
    
    qc << RZ(target, 2 * time)
    
    for i in reversed(non_i):
        if i != target:
            qc << CNOT(i, target)
    
    for i in reversed(non_i):
        p = pauli_string[i]
        if p == 'X':
            qc << H(i)
        elif p == 'Y':
            qc << RX(i, -np.pi / 2)
    
    return qc
