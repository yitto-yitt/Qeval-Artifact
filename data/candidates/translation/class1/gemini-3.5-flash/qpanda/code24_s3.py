# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import *

def dj_algorithm(oracle):
    machine = get_global_machine()
    qubits = get_all_used_qubits(oracle)
    qubits.sort(key=lambda q: q.get_phy_addr())
    
    prog = QProg()
    prog << X(qubits[-1])
    for q in qubits:
        prog << H(q)
    prog << oracle
    for q in qubits:
        prog << H(q)
        
    measure_qubits = qubits[:-1][::-1]
    probs = machine.prob_run_dict(prog, measure_qubits)
    return probs
