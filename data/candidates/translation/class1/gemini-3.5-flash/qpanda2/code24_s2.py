# EVAL_META: task_id=24, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def dj_algorithm(oracle):
    qubits = get_all_used_qubits(oracle)
    qubits = sorted(qubits, key=lambda q: q.get_phy_addr())
    n = len(qubits)
    
    prog = QProg()
    prog << X(qubits[n - 1])
    for q in qubits:
        prog << H(q)
    prog << oracle
    for q in qubits:
        prog << H(q)
        
    cbits = c_alloc_many(n - 1)
    for i in range(n - 1):
        prog << Measure(qubits[i], cbits[i])
        
    result = run_with_configuration(prog, cbits, 1000)
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
