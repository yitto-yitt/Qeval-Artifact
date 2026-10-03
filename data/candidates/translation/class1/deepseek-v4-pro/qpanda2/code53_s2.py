# EVAL_META: task_id=53, framework=qpanda2, class=1
from pyqpanda import *

def xor_gate(a, b):
    init(QMachineType.CPU)
    q = qAlloc_many(8)
    c = cAlloc_many(8)
    prog = QProg()

    for i in range(8):
        if (a >> i) & 1:
            prog << X(q[i])
        if (b >> i) & 1:
            prog << X(q[i])

    for i in range(8):
        prog << Measure(q[i], c[i])

    shots = 1024
    counts = run_with_configuration(prog, c, shots)
    finalize()

    return {key.replace(' ', ''): value / shots for key, value in counts.items()}
