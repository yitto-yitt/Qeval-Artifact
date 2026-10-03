# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, Toffoli, Measure

def or_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qr_a = qvm.qAlloc_many(3)
    qr_b = qvm.qAlloc_many(3)
    ancillary = qvm.qAlloc_many(3)
    measure = qvm.cAlloc_many(3)

    prog = QProg()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')

    for i in range(3):
        if a_bin[2 - i] == '0':
            prog << X(qr_a[i])
        if b_bin[2 - i] == '0':
            prog << X(qr_b[i])

    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])

    for i in range(3):
        prog << X(ancillary[i])

    for i in range(3):
        prog << Measure(ancillary[i], measure[i])

    result = qvm.run_with_configuration(prog, measure, 1024)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
