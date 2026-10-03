# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import *

def or_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()

    q = machine.qAlloc_many(9)
    c = machine.cAlloc_many(3)

    prog = QProg()

    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    for i in range(3):
        if a_bits[2 - i] == '0':
            prog << X(q[i])
        if b_bits[2 - i] == '0':
            prog << X(q[3 + i])

    for i in range(3):
        prog << Toffoli(q[i], q[3 + i], q[6 + i])

    for i in range(3):
        prog << X(q[6 + i])

    for i in range(3):
        prog << Measure(q[6 + i], c[i])

    shots = 1000
    counts = machine.run_with_configuration(prog, c, shots)
    machine.finalize()

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
