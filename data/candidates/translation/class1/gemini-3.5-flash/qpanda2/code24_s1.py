# EVAL_META: task_id=24, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def dj_algorithm(oracle):
    # We assume the global machine is already initialized because the oracle exists.
    prog = QProg()
    prog << oracle
    
    # Get all used qubits and sort them by physical address
    qubits = sorted(get_all_used_qubits(prog), key=lambda q: q.get_phy_addr())
    n = len(qubits)
    
    # Allocate classical bits
    cbits = c_alloc_many(n - 1)
    
    # Build the Deutsch-Jozsa routine
    dj_prog = QProg()
    dj_prog << X(qubits[-1])
    for q in qubits:
        dj_prog << H(q)
        
    dj_prog << oracle
    
    for q in qubits:
        dj_prog << H(q)
        
    for i in range(n - 1):
        dj_prog << Measure(qubits[i], cbits[i])
        
    # Run and get counts
    shots = 1000
    counts = run_with_configuration(dj_prog, shots)
    
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
