# EVAL_META: task_id=120, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)

def create_diagonal_circuit(diag):
    n = int(np.round(np.log2(len(diag))))
    if 2**n != len(diag):
        raise ValueError("diag length must be a power of 2")
    
    q = qubits[:n]
    prog = pq.QProg()
    circ = pq.QCircuit()
    
    diag_arr = np.array(diag, dtype=complex)
    thetas = np.angle(diag_arr)
    
    for S in range(1, 2**n):
        S_qubits = [i for i in range(n) if (S & (1 << i))]
        
        alpha_S = 0.0
        for x in range(2**n):
            dot = bin(x & S).count('1') % 2
            sign = 1 if dot == 0 else -1
            alpha_S += sign * thetas[x]
            
        alpha_S = -alpha_S / (2**(n - 1))
        
        if abs(alpha_S) < 1e-12:
            continue
            
        if len(S_qubits) == 1:
            circ << pq.RZ(q[S_qubits[0]], alpha_S)
        else:
            for i in range(len(S_qubits) - 1):
                circ << pq.CNOT(q[S_qubits[i]], q[S_qubits[i+1]])
            circ << pq.RZ(q[S_qubits[-1]], alpha_S)
            for i in range(len(S_qubits) - 2, -1, -1):
                circ << pq.CNOT(q[S_qubits[i]], q[S_qubits[i+1]])
                
    prog.insert(circ)
    return prog

machine.finalize()
