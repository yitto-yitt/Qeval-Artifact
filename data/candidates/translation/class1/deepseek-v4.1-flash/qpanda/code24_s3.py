# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import *

def dj_algorithm(oracle):
    n = oracle.get_qubit_num()
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(n)
    c = qvm.cAlloc_many(n - 1)
    prog = QProg()
    prog << X(q[n - 1])
    for i in range(n):
        prog << H(q[i])
    prog << oracle
    for i in range(n):
        prog << H(q[i])
    for i in range(n - 1):
        prog << measure(q[i], c[i])
    shots = 1024
    counts = qvm.run_with_configuration(prog, c, shots)
    total = sum(counts.values())
    result = {}
    for k, v in counts.items():
        if isinstance(k, int):
            key = format(k, f'0{n-1}b')
        else:
            key = k
        result[key] = v / total
    return result
