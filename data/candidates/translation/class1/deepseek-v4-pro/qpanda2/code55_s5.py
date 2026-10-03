# EVAL_META: task_id=55, framework=qpanda2, class=1
from pyqpanda import *

def or_gate(a, b):
    init(QMachineType.CPU)

    q = qAlloc_many(9)
    c = cAlloc_many(3)

    prog = QProg()

    a_bin = format(a, '03b')
    b_bin = format(b, '03b')

    for i in range(3):
        if a_bin[2 - i] == '0':
            prog << X(q[i])
        if b_bin[2 - i] == '0':
            prog << X(q[3 + i])

    for i in range(3):
        prog << Toffoli(q[i], q[3 + i], q[6 + i])

    prog << X(q[6]) << X(q[7]) << X(q[8])

    for i in range(3):
        prog << Measure(q[6 + i], c[i])

    shots = 1024
    counts = run_with_configuration(prog, c, shots)

    destroyQuantumMachine()

    return {key: value / shots for key, value in counts.items()}
