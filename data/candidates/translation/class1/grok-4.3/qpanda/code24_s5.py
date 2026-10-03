# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import *

def dj_algorithm(oracle):
    n = oracle.num_qubits
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)
    c = machine.cAlloc_many(n - 1)
    prog = QProg()
    prog << X(q[n - 1])
    for i in range(n):
        prog << H(q[i])
    prog << oracle
    for i in range(n):
        prog << H(q[i])
    prob_result = machine.prob_run_dict(prog, q[:n-1])
    total = sum(prob_result.values())
    return {key: value / total for key, value in prob_result.items()}
