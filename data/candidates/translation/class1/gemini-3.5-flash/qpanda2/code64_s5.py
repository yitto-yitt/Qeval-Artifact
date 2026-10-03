# EVAL_META: task_id=64, framework=qpanda2, class=1
from pyqpanda import *


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

    prog << BARRIER(q)

    for k in range(n):
        prog << CNOT(q[k], q[n + k])

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(q[i], q[n + j])
        prog << BARRIER(q)
        for k in range(n):
            prog << H(q[k])

    for k in range(n):
        prog << Measure(q[k], c[k])

    prog.machine = machine
    return prog
