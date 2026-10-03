# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import QProg, qalloc, H, X, Statevector
import numpy as np

def dj_algorithm(oracle):
    n = getattr(oracle, 'num_qubits', None)
    if n is None:
        n = getattr(oracle, 'qubit_num', None)
    if n is None:
        n = len(oracle)
        
    q = qalloc(n)
    prog = QProg()
    prog << X(q[n - 1])
    for i in range(n):
        prog << H(q[i])
        
    prog << oracle
    
    for i in range(n):
        prog << H(q[i])
        
    sv = Statevector(prog)
    
    try:
        probs = sv.get_probabilities()
    except AttributeError:
        try:
            probs = sv.probabilities()
        except AttributeError:
            probs = np.abs(np.array(sv.data))**2
            
    dist = {}
    for i, p in enumerate(probs):
        if p > 1e-9:
            prefix = i >> 1
            bit_str = format(prefix, f'0{n-1}b')
            dist[bit_str] = dist.get(bit_str, 0.0) + p
            
    total = sum(dist.values())
    if total > 0:
        dist = {k: v / total for k, v in dist.items()}
        
    return dist
