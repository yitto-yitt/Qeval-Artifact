# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import BARRIER, CNOT, CPUQVM, H, Measure, QProg


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    machine = CPUQVM()
    machine.init_qvm()

    q_reg1 = machine.qAlloc_many(n)
    q_reg2 = machine.qAlloc_many(n)
    c_reg = machine.cAlloc_many(n)

    prog = QProg()

    for q in q_reg1:
        prog << H(q)

    prog << BARRIER(q_reg1 + q_reg2)

    for q1, q2 in zip(q_reg1, q_reg2):
        prog << CNOT(q1, q2)

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(q_reg1[i], q_reg2[j])
        prog << BARRIER(q_reg1 + q_reg2)
        for q in q_reg1:
            prog << H(q)

    for q, c in zip(q_reg1, c_reg):
        prog << Measure(q, c)

    return prog
