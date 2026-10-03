# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import *

def dj_algorithm(oracle):
    n = oracle.num_qubits
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    prog = QProg()
    prog << X(qubits[n-1])
    for i in range(n):
        prog << H(qubits[i])
    prog << oracle
    for i in range(n):
        prog << H(qubits[i])
    prob_dict = qvm.prob_run_dict(prog, qubits[:n-1])
    return prob_dict
