# EVAL_META: task_id=54, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def and_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qr_a = qvm.qAlloc_many(3)
    qr_b = qvm.qAlloc_many(3)
    ancillary = qvm.qAlloc_many(3)
    measure = qvm.cAlloc_many(3)
    prog = QProg()
    a = format(a, '03b')
    b = format(b, '03b')
    for i in range(3):
        if a[2-i] == '1':
            prog.insert(X(qr_a[i]))
        if b[2-i] == '1':
            prog.insert(X(qr_b[i]))
    for i in range(3):
        prog.insert(CCNOT(qr_a[i], qr_b[i], ancillary[i]))
    for i in range(3):
        prog.insert(Measure(ancillary[i], measure[i]))
    shots = 1024
    counts = qvm.run_with_configuration(prog, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
