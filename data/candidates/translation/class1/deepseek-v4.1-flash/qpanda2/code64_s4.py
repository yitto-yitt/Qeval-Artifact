# EVAL_META: task_id=64, framework=qpanda2, class=1
from pyqpanda import *

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    q1 = [Qubit(i) for i in range(n)]
    q2 = [Qubit(n + i) for i in range(n)]
    c = [CBit(i) for i in range(n)]
    prog = QProg()
    for q in q1:
        prog << H(q)
    prog << BARRIER(q1 + q2)
    for j in range(n):
        prog << CNOT(q1[j], q2[j])
    if '1' in s:
        i = s.find('1')
        for j in range(n):
            if s[j] == '1':
                prog << CNOT(q1[i], q2[j])
        prog << BARRIER(q1 + q2)
        for q in q1:
            prog << H(q)
    for j in range(n):
        prog << Measure(q1[j], c[j])
    return prog
