# EVAL_META: task_id=54, framework=qpanda, class=1

from pyqpanda3.core import CPUQVM, QProg, X, Toffoli, measure

def and_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(9)
    c = qvm.cAlloc_many(3)
    prog = QProg()

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    for i in range(3):
        if a_bits[2 - i] == '1':
            prog << X(q[i])
        if b_bits[2 - i] == '1':
            prog << X(q[i + 3])

    for i in range(3):
        prog << Toffoli(q[i], q[i + 3], q[i + 6])

    for i in range(3):
        prog << measure(q[i + 6], c[i])

    counts = qvm.run_with_configuration(prog, c, 1024)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
