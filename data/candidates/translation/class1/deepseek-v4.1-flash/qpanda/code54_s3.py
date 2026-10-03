# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import QProg, Qubit, CBit, X, Toffoli, measure, CPUQVM


def and_gate(a, b):
    prog = QProg()

    qr_a = [Qubit(i) for i in range(3)]
    qr_b = [Qubit(i + 3) for i in range(3)]
    ancillary = [Qubit(i + 6) for i in range(3)]
    cbits = [CBit(i) for i in range(3)]

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
        prog << measure(ancillary[i], cbits[i])

    qvm = CPUQVM()
    qvm.run(prog, 1024)
    counts = qvm.result().get_counts()

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
