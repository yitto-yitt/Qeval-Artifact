# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, QCircuit, X, Toffoli, measure

def or_gate(a, b):
    a = format(a, '03b')
    b = format(b, '03b')
    qr_a = [0, 1, 2]
    qr_b = [3, 4, 5]
    ancillary = [6, 7, 8]

    circ = QCircuit()
    for i in range(3):
        if a[2 - i] == '0':
            circ << X(qr_a[i])
        if b[2 - i] == '0':
            circ << X(qr_b[i])
    for i in range(3):
        circ << Toffoli(qr_a[i], qr_b[i], ancillary[i])
    for i in range(3):
        circ << X(ancillary[i])

    prog = QProg()
    prog << circ
    for i in range(3):
        prog << measure(ancillary[i], i)

    qvm = CPUQVM()
    qvm.run(prog, 1024)
    counts = qvm.result().get_counts()

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
