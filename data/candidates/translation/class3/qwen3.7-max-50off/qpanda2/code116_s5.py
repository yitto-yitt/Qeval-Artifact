# EVAL_META: task_id=116, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(64)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    prog = pq.QProg()
    
    active_qubits = []
    for i, p in enumerate(pauli_string):
        if p != 'I':
            qubit_idx = n - 1 - i
            active_qubits.append((qubit_idx, p))
            
    if not active_qubits:
        return prog

    for i, p in active_qubits:
        if p == 'X':
            prog << pq.H(qubits[i])
        elif p == 'Y':
            prog << pq.H(qubits[i])
            prog << pq.Sdag(qubits[i])
            
    if len(active_qubits) > 1:
        for j in range(len(active_qubits) - 1):
            ctrl_idx = active_qubits[j][0]
            targ_idx = active_qubits[j+1][0]
            prog << pq.CNOT(qubits[ctrl_idx], qubits[targ_idx])
            
    target_idx = active_qubits[-1][0]
    prog << pq.RZ(qubits[target_idx], 2 * time)
    
    if len(active_qubits) > 1:
        for j in range(len(active_qubits) - 2, -1, -1):
            ctrl_idx = active_qubits[j][0]
            targ_idx = active_qubits[j+1][0]
            prog << pq.CNOT(qubits[ctrl_idx], qubits[targ_idx])
            
    for i, p in reversed(active_qubits):
        if p == 'X':
            prog << pq.H(qubits[i])
        elif p == 'Y':
            prog << pq.S(qubits[i])
            prog << pq.H(qubits[i])
            
    return prog

machine.finalize()
