# EVAL_META: task_id=64, framework=qpanda2, class=1
from pyqpanda import *


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    q1 = qAlloc_many(n, "reg1")
    q2 = qAlloc_many(n, "reg2")
    c = cAlloc_many(n, "c")

    prog = QProg()

    for i in range(n):
        prog << H(q1[i])

    prog << BARRIER(q1)

    for i in range(n):
        prog << CNOT(q1[i], q2[i])

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(q1[i], q2[j])

        prog << BARRIER(q1)

        for k in range(n):
            prog << H(q1[k])

    for k in range(n):
        prog << Measure(q1[k], c[k])

    return prog
