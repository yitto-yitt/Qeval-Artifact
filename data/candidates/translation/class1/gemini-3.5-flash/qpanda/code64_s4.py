# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import *


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    machine = CPUQVM()
    machine.init_qvm()

    q = machine.qAlloc_many(2 * n)
    c = machine.cAlloc_many(n)

    prog = QProg()

    for i in range(n):
        prog << H(q[i])

    for i in range(n):
        prog << CNOT(q[i], q[n + i])

    if "1" in s:
        idx = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(q[idx], q[n + j])
        for i in range(n):
            prog << H(q[i])

    for i in range(n):
        prog << Measure(q[i], c[i])

    return prog
