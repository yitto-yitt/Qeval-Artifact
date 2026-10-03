# EVAL_META: task_id=120, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np
import cmath

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def create_diagonal_circuit(diag):
    n = int(round(np.log2(len(diag))))
    q = qubits[:n]
    prog = pq.QProg()
    
    if n == 0:
        return prog

    theta = [cmath.phase(complex(d)) for d in diag]
    
    for S in range(1, 1 << n):
        alpha_S = 0.0
        for k in range(1 << n):
            parity = bin(k & S).count('1') % 2
            if parity == 0:
                alpha_S += theta[k]
            else:
                alpha_S -= theta[k]
        alpha_S /= (1 << n)
        
        if abs(alpha_S) > 1e-12:
            S_qubits = [i for i in range(n) if (S & (1 << i))]
            t = S_qubits[-1]
            controls = S_qubits[:-1]
            
            for c in controls:
                prog << pq.CNOT(q[c], q[t])
                
            prog << pq.RZ(q[t], -2.0 * alpha_S)
            
            for c in controls:
                prog << pq.CNOT(q[c], q[t])
                
    return prog

machine.finalize()
