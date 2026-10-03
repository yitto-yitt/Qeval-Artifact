# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import *


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAllocMany(2 * n)
    c = machine.cAllocMany(n)

    prog = QProg()
    for i in range(n):
        prog << H(q[i])

    prog << BARRIER(q)

    for i in range(n):
        prog << CNOT(q[i], q[n + i])

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(q[i], q[n + j])
        prog << BARRIER(q)
        for j in range(n):
            prog << H(q[j])

    for j in range(n):
        prog << Measure(q[j], c[j])

    return prog
