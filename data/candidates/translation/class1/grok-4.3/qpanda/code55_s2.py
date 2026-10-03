# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import *
def or_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qa = qvm.qAlloc_many(3)
    qb = qvm.qAlloc_many(3)
    anc = qvm.qAlloc_many(3)
    cb = qvm.cAlloc_many(3)
    prog = QProg()
    astr = format(a, '03b')
    bstr = format(b, '03b')
    for i in range(3):
        if astr[2-i] == '0':
            prog << X(qa[i])
        if bstr[2-i] == '0':
            prog << X(qb[i])
    for i in range(3):
        prog << Toffoli(qa[i], qb[i], anc[i])
    for i in range(3):
        prog << X(anc[i])
    prog << measure(anc, cb)
    result = qvm.run_with_shots(prog, 1024)
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v/total for k, v in counts.items()}
