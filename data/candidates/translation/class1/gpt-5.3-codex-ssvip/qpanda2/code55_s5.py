# EVAL_META: task_id=55, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def or_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qr_a = qvm.qAlloc_many(3)
    qr_b = qvm.qAlloc_many(3)
    ancillary = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    prog = QProg()

    for i in range(3):
        if a_bits[2 - i] == '0':
            prog << X(qr_a[i])
        if b_bits[2 - i] == '0':
            prog << X(qr_b[i])

    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])

    for i in range(3):
        prog << X(ancillary[i])

    for i in range(3):
        prog << Measure(ancillary[i], cbits[i])

    shots = 1000
    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    qvm.finalize()
    return probs
