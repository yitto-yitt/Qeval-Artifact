# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QProg, Qubit, CNOT, RZ

def create_diagonal_circuit(diag):
    n = int(np.round(np.log2(len(diag))))
    qubits = [Qubit() for _ in range(n)]
    prog = QProg()
    
    phases = np.angle(diag)
    
    alphas = {}
    for S in range(1, 1 << n):
        alpha = 0.0
        for k in range(1 << n):
            dot = bin(k & S).count('1') % 2
            sign = 1 if dot == 0 else -1
            alpha += phases[k] * sign
        alpha /= (1 << n)
        if abs(alpha) > 1e-10:
            alphas[S] = alpha
            
    for S, alpha in alphas.items():
        S_qubits = [i for i in range(n) if (S & (1 << i))]
        target = S_qubits[-1]
        controls = S_qubits[:-1]
        
        for c in controls:
            prog << CNOT(qubits[c], qubits[target])
            
        prog << RZ(qubits[target], -2.0 * alpha)
        
        for c in reversed(controls):
            prog << CNOT(qubits[c], qubits[target])
            
    return prog
