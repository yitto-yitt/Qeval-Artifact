# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import *

def or_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    qr_a = machine.qAlloc_many(3)
    qr_b = machine.qAlloc_many(3)
    ancillary = machine.qAlloc_many(3)
    cr = machine.cAlloc_many(3)

    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

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
        prog << Measure(ancillary[i], cr[i])

    shots = 1024
    counts = machine.run_with_configuration(prog, cr, shots)

    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    machine.finalize()
    return probs
