# EVAL_META: task_id=54, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def and_gate(a, b):
    init(QMachineType.CPU)

    qr_a = qAlloc_many(3)
    qr_b = qAlloc_many(3)
    ancillary = qAlloc_many(3)
    measure = cAlloc_many(3)

    prog = QProg()

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    for i in range(3):
        if a_bits[2 - i] == '1':
            prog << X(qr_a[i])
        if b_bits[2 - i] == '1':
            prog << X(qr_b[i])

    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])

    for i in range(3):
        prog << Measure(ancillary[i], measure[i])

    shots = 1024
    counts = run_with_configuration(prog, measure, shots)
    total = builtins.sum(counts.values())

    return {key: value / total for key, value in counts.items()}
