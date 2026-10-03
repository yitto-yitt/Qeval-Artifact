# EVAL_META: task_id=64, framework=qpanda2, class=1
from pyqpanda import *

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    init(QMachineType.CPU)
    q1 = qAlloc_many(n)
    q2 = qAlloc_many(n)
    c = cAlloc_many(n)
    prog = QProg()
    for j in range(n):
        prog.insert(H(q1[j]))
    for j in range(n):
        prog.insert(CNOT(q1[j], q2[j]))
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog.insert(CNOT(q1[i], q2[j]))
        for j in range(n):
            prog.insert(H(q1[j]))
    for j in range(n):
        prog.insert(Measure(q1[j], c[j]))
    return prog
