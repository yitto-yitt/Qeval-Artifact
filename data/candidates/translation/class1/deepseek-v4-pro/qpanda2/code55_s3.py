# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def or_gate(a, b):
    init(QMachineType.CPU)

    qr_a = qAlloc_many(3)
    qr_b = qAlloc_many(3)
    ancillary = qAlloc_many(3)
    measure = cAlloc_many(3)

    prog = QProg()

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    for i in range(3):
        if a_bits[2 - i] == '0':
            prog << X(qr_a[i])
        if b_bits[2 - i] == '0':
            prog << X(qr_b[i])

    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])

    for i in range(3):
        prog << X(ancillary[i])

    prog << Measure(ancillary[2], measure[0])
    prog << Measure(ancillary[1], measure[1])
    prog << Measure(ancillary[0], measure[2])

    shots = 1024
    counts = run_with_configuration(prog, measure, shots)
    total = builtins.sum(counts.values())

    return {key: value / total for key, value in counts.items()}
