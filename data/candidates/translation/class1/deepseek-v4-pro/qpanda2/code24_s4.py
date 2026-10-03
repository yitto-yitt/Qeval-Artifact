# EVAL_META: task_id=24, framework=qpanda2, class=1
from pyqpanda import *

def dj_algorithm(oracle):
    if hasattr(oracle, "qvec"):
        q = list(oracle.qvec)
    elif hasattr(oracle, "get_qubits"):
        q = list(oracle.get_qubits())
    elif hasattr(oracle, "getQubitVec"):
        q = list(oracle.getQubitVec())
    else:
        raise AttributeError("oracle must expose qubits")

    n = len(q)
    prog = QProg()
    prog << X(q[n - 1])
    for i in range(n):
        prog << H(q[i])

    if hasattr(oracle, "to_qprog"):
        prog << oracle.to_qprog()
    else:
        prog << oracle

    for i in range(n):
        prog << H(q[i])

    return prob_run_dict(prog, q[:-1])
