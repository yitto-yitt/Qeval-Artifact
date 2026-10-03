# EVAL_META: task_id=64, framework=qpanda2, class=1
from pyqpanda import *


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    q1 = qAlloc_many(n)
    q2 = qAlloc_many(n)
    c = cAlloc_many(n)

    prog = QProg()

    for k in range(n):
        prog << H(q1[k])

    for k in range(n):
        prog << CNOT(q1[k], q2[k])

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(q1[i], q2[j])

        for k in range(n):
            prog << H(q1[k])

    for k in range(n):
        prog << Measure(q1[k], c[k])

    return prog
