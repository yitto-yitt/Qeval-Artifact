# EVAL_META: task_id=116, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init()
qubits = machine.qAlloc_many(32)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    prog = pq.QProg()
    
    active_qubits = []
    for i, p in enumerate(reversed(pauli_string)):
        if p != 'I':
            active_qubits.append((i, p))
            
    if not active_qubits:
        return prog
        
    for idx, p in active_qubits:
        if p == 'X':
            prog << pq.H(qubits[idx])
        elif p == 'Y':
            prog << pq.S(qubits[idx]).dagger() << pq.H(qubits[idx])
            
    if len(active_qubits) > 1:
        for i in range(len(active_qubits) - 1):
            prog << pq.CNOT(qubits[active_qubits[i][0]], qubits[active_qubits[i+1][0]])
            
    last_q = active_qubits[-1][0]
    prog << pq.RZ(qubits[last_q], 2.0 * time)
    
    if len(active_qubits) > 1:
        for i in range(len(active_qubits) - 2, -1, -1):
            prog << pq.CNOT(qubits[active_qubits[i][0]], qubits[active_qubits[i+1][0]])
            
    for idx, p in active_qubits:
        if p == 'X':
            prog << pq.H(qubits[idx])
        elif p == 'Y':
            prog << pq.H(qubits[idx]) << pq.S(qubits[idx])
            
    return prog

machine.finalize()
