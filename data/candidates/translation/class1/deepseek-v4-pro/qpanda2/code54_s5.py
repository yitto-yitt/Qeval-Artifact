# EVAL_META: task_id=54, framework=qpanda2, class=1
from pyqpanda import *

def and_gate(a, b):
    a = format(a, '03b')
    b = format(b, '03b')
    init_qvm(QMachineType.CPU)
    qr_a = qAlloc_many(3)
    qr_b = qAlloc_many(3)
    ancillary = qAlloc_many(3)
    measure = cAlloc_many(3)
    prog = QProg()

    for i in range(3):
        if a[2 - i] == '1':
            prog << X(qr_a[i])
        if b[2 - i] == '1':
            prog << X(qr_b[i])

    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])

    for i in range(3):
        prog << Measure(ancillary[i], measure[i])

    shots = 1024
    counts = run_with_configuration(prog, measure, shots)
    finalize_qvm()
    return {key: float(value / shots) for key, value in counts.items()}
