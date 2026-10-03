# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QCircuit, QProg, X, Toffoli

def or_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qr_a = qvm.qAlloc_many(3)
    qr_b = qvm.qAlloc_many(3)
    ancillary = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    a_str = format(a, '03b')
    b_str = format(b, '03b')

    circ = QCircuit()
    for i in range(3):
        if a_str[2 - i] == '0':
            circ << X(qr_a[i])
        if b_str[2 - i] == '0':
            circ << X(qr_b[i])
    for i in range(3):
        circ << Toffoli(qr_a[i], qr_b[i], ancillary[i])
    for i in range(3):
        circ << X(ancillary[i])

    prog = QProg()
    prog << circ
    for i in range(3):
        prog << pyqpanda_measure(ancillary[i], cbits[i])

    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    qvm.finalize()
    return {key: value / total for key, value in counts.items()}


def pyqpanda_measure(q, c):
    from pyqpanda import Measure
    return Measure(q, c)
