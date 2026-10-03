# EVAL_META: task_id=55, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def or_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qa = qvm.qAlloc_many(3)
    qb = qvm.qAlloc_many(3)
    qanc = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    prog = QProg()
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    for i in range(3):
        if a_str[2 - i] == '0':
            prog.insert(X(qa[i]))
        if b_str[2 - i] == '0':
            prog.insert(X(qb[i]))
    for i in range(3):
        prog.insert(CCX(qa[i], qb[i], qanc[i]))
    for i in range(3):
        prog.insert(X(qanc[i]))
    for i in range(3):
        prog.insert(Measure(qanc[i], c[i]))
    shots = 1024
    result = qvm.run_with_configuration(prog, c, shots)
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
