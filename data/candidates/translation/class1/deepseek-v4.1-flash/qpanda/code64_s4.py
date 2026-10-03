# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QProg, Qubit, CBit, H, CNOT, Measure, BARRIER

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    prog = QProg()
    q = Qubit(2 * n)
    c = CBit(n)
    for i in range(n):
        prog << H(q[i])
    prog << BARRIER(q)
    for i in range(n):
        prog << CNOT(q[i], q[n + i])
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(q[i], q[n + j])
        prog << BARRIER(q)
        for i in range(n):
            prog << H(q[i])
    for i in range(n):
        prog << Measure(q[i], c[i])
    return prog
