# EVAL_META: task_id=116, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QProg, H, RX, RZ, CNOT, qAlloc_many

machine = CPUQVM()
machine.init()
qubits = qAlloc_many(32)

def synthesize_evolution_gate(pauli_string, time):
    prog = QProg()
    n = len(pauli_string)
    q = qubits[:n]
    
    for i, p in enumerate(pauli_string):
        if p == 'X':
            prog << H(q[i])
        elif p == 'Y':
            prog << RX(q[i], np.pi / 2)
            
    active_qubits = [i for i, p in enumerate(pauli_string) if p != 'I']
    
    if len(active_qubits) > 0:
        for i in range(len(active_qubits) - 1):
            prog << CNOT(q[active_qubits[i]], q[active_qubits[i+1]])
            
        prog << RZ(q[active_qubits[-1]], 2 * time)
        
        for i in range(len(active_qubits) - 2, -1, -1):
            prog << CNOT(q[active_qubits[i]], q[active_qubits[i+1]])
            
    for i, p in enumerate(pauli_string):
        if p == 'X':
            prog << H(q[i])
        elif p == 'Y':
            prog << RX(q[i], -np.pi / 2)
            
    return prog

machine.finalize()
