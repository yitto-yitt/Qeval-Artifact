# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import *
import math

def dj_algorithm(oracle):
    n = oracle.get_qubit_num()
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

    for i in range(n - 1):
        prog << Measure(q[i], c[i])

    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    machine.finalize()
    return probs
