# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import *

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2 * n)
    c = qvm.cAlloc_many(n)

    reg1 = q[:n]
    reg2 = q[n:]

    prog = QProg()

    for i in range(n):
        prog << H(reg1[i])

    for i in range(n):
        prog << CNOT(reg1[i], reg2[i])

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(reg1[i], reg2[j])
        for k in range(n):
            prog << H(reg1[k])

    for i in range(n):
        prog << Measure(reg1[i], c[i])

    qvm.run_with_configuration(prog, c, 1024)
    return prog
