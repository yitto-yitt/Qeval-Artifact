# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, measure

def xor_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(8)
    c = qvm.cAlloc_many(8)
    prog = QProg()
    for i in range(8):
        if (a >> i) & 1:
            prog << X(q[i])
    for i in range(8):
        if (b >> i) & 1:
            prog << X(q[i])
    for i in range(8):
        prog << measure(q[i], c[i])
    result = qvm.run(prog, 1000)
    counts = {}
    for k, v in result.items():
        if isinstance(k, int):
            key = format(k, '08b')
        else:
            key = str(k).zfill(8)
        counts[key] = counts.get(key, 0) + v
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
