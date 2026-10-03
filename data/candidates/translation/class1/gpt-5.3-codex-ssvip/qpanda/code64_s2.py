# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import *

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    qvm = CPUQVM()
    qvm.init_qvm()
    q_reg1 = qvm.qAlloc_many(n)
    q_reg2 = qvm.qAlloc_many(n)
    c_reg = qvm.cAlloc_many(n)

    prog = QProg()
    for i in range(n):
        prog << H(q_reg1[i])

    for i in range(n):
        prog << CNOT(q_reg1[i], q_reg2[i])

    if "1" in s:
        i0 = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(q_reg1[i0], q_reg2[j])
        for i in range(n):
            prog << H(q_reg1[i])

    for i in range(n):
        prog << Measure(q_reg1[i], c_reg[i])

    return prog
