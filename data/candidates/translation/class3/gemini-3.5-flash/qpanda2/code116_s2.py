# EVAL_META: task_id=116, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

# Initialize Global QVM
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(100)

def synthesize_evolution_gate(pauli_string, time):
    N = len(pauli_string)
    active = []
    for i in range(N):
        op = pauli_string[N - 1 - i]
        if op != 'I':
            active.append((i, op))
            
    prog = pq.QCircuit()
    if not active:
        return prog
        
    # 1. Basis change before
    for idx, op in active:
        if op == 'X':
            prog << pq.H(q[idx])
        elif op == 'Y':
            prog << pq.RX(q[idx], np.pi / 2)
            
    # 2. CNOT chain
    for j in range(len(active) - 1):
        prog << pq.CNOT(q[active[j][0]], q[active[j+1][0]])
        
    # 3. RZ gate on the last active qubit
    last_idx = active[-1][0]
    prog << pq.RZ(q[last_idx], 2 * time)
    
    # 4. Reverse CNOT chain
    for j in range(len(active) - 2, -1, -1):
        prog << pq.CNOT(q[active[j][0]], q[active[j+1][0]])
        
    # 5. Reverse basis change
    for idx, op in active:
        if op == 'X':
            prog << pq.H(q[idx])
        elif op == 'Y':
            prog << pq.RX(q[idx], -np.pi / 2)
            
    return prog

# Manual Cleanup
machine.finalize()
