# EVAL_META: task_id=54, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def and_gate(a, b):
    init(QMachineType.CPU)
    q_a = qAlloc_many(3)
    q_b = qAlloc_many(3)
    anc = qAlloc_many(3)
    c = cAlloc_many(3)
    prog = QProg()

    a_str = format(a, '03b')
    b_str = format(b, '03b')

    for i in range(3):
        if a_str[2 - i] == '1':
            prog << X(q_a[i])
        if b_str[2 - i] == '1':
            prog << X(q_b[i])

    for i in range(3):
        prog << Toffoli(q_a[i], q_b[i], anc[i])

    prog << measure(anc[0], c[0])
    prog << measure(anc[1], c[1])
    prog << measure(anc[2], c[2])

    shots = 1024
    counts = run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
