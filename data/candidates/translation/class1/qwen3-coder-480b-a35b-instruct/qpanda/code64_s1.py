# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda import *


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    machine = init(QMachineType.CPU)
    q_reg1 = machine.qAlloc_many(n)
    q_reg2 = machine.qAlloc_many(n)
    c_reg = machine.cAlloc_many(n)
    prog = QProg()
    prog.insert(H(q_reg1))
    prog.insert(BARRIER(q_reg1 + q_reg2))
    for i in range(n):
        prog.insert(CNOT(q_reg1[i], q_reg2[i]))
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog.insert(CNOT(q_reg1[i], q_reg2[j]))
        prog.insert(BARRIER(q_reg1 + q_reg2))
        prog.insert(H(q_reg1))
    for i in range(n):
        prog.insert(MEASURE(q_reg1[i], c_reg[i]))
    return prog
