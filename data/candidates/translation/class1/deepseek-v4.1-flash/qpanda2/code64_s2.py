# EVAL_META: task_id=64, framework=qpanda2, class=1
from pyqpanda import QProg, Qubit, CBit, H, CNOT, Measure, Barrier

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    q_reg1 = [Qubit(i) for i in range(n)]
    q_reg2 = [Qubit(i + n) for i in range(n)]
    c_reg = [CBit(i) for i in range(n)]
    prog = QProg()
    for q in q_reg1:
        prog << H(q)
    prog << Barrier(q_reg1 + q_reg2)
    for i in range(n):
        prog << CNOT(q_reg1[i], q_reg2[i])
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(q_reg1[i], q_reg2[j])
        prog << Barrier(q_reg1 + q_reg2)
        for q in q_reg1:
            prog << H(q)
    for i in range(n):
        prog << Measure(q_reg1[i], c_reg[i])
    return prog

