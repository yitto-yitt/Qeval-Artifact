# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import *
def dj_algorithm(oracle):
    n = oracle.num_qubits
    qvm = CPUQVM()
    qvm.init_qvm()
    qs = qvm.qAlloc_many(n)
    prog = QProg()
    prog << X(qs[n-1])
    for i in range(n):
        prog << H(qs[i])
    prog << oracle
    for i in range(n):
        prog << H(qs[i])
    result = qvm.prob_run_dict(prog, qs[:n-1])
    return result
