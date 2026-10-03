# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, CCX, measure

def or_gate(a, b):
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(9)
    c = qvm.cAlloc_many(3)
    prog = QProg()
    for i in range(3):
        if a_bin[2 - i] == '0':
            prog << X(q[i])
        if b_bin[2 - i] == '0':
            prog << X(q[3 + i])
    for i in range(3):
        prog << CCX(q[i], q[3 + i], q[6 + i])
    for i in range(3):
        prog << X(q[6 + i])
    for i in range(3):
        prog << measure(q[6 + i], c[i])
    result = qvm.run_with_configuration(prog, c, 1000)
    qvm.finalize()
    counts = {}
    for key, val in result.items():
        if isinstance(key, int):
            k = format(key, '03b')
        else:
            k = key
        counts[k] = val
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
