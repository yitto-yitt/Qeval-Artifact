# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, Measure

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2 * n)
    c = qvm.cAlloc_many(n)
    prog = QProg()
    for i in range(n):
        prog << H(q[i])
    for i in range(n):
        prog << CNOT(q[i], q[n + i])
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(q[i], q[n + j])
        for i in range(n):
            prog << H(q[i])
    for i in range(n):
        prog << Measure(q[i], c[i])
    return prog
