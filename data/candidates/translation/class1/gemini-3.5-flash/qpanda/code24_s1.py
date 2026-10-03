# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import *

def dj_algorithm(oracle):
    qubits = oracle.get_used_qubits()
    qubits.sort(key=lambda q: q.get_phy_addr())
    n = len(qubits)
    
    try:
        machine = get_current_quantum_machine()
    except Exception:
        machine = CPUQVM()
        machine.init_qvm()
        
    prog = QProg()
    prog << X(qubits[n-1])
    for q in qubits:
        prog << H(q)
    prog << oracle
    for q in qubits:
        prog << H(q)
        
    measure_qubits = qubits[:-1][::-1]
    result = machine.prob_run_dict(prog, measure_qubits, -1)
    return result
