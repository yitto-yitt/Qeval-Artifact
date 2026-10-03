# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda import *

def dj_algorithm(oracle):
    machine = GetQuantumMachine()
    prog_oracle = QProg(oracle)
    q_list = get_all_used_qubits(prog_oracle)
    q_list.sort(key=lambda q: q.get_phy_addr())
    n = len(q_list)
    
    prog = QProg()
    prog << X(q_list[n-1])
    for q in q_list:
        prog << H(q)
    prog << oracle
    for q in q_list:
        prog << H(q)
        
    meas_qubits = list(reversed(q_list[:-1]))
    res = machine.prob_run_dict(prog, meas_qubits)
    return res
