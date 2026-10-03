# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, X, Toffoli

def or_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qr_a = qvm.qAlloc_many(3)
    qr_b = qvm.qAlloc_many(3)
    ancillary = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    a = format(a, '03b')
    b = format(b, '03b')

    prog = qvm.qProg() if hasattr(qvm, 'qProg') else None
    from pyqpanda import QProg
    prog = QProg()

    for i in range(3):
        if a[2 - i] == '0':
            prog << X(qr_a[i])
        if b[2 - i] == '0':
            prog << X(qr_b[i])

    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])

    for i in range(3):
        prog << X(ancillary[i])

    for i in range(3):
        prog << pyqpanda_measure(ancillary[i], cbits[i])

    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    qvm.finalize()
    return {key: value / total for key, value in counts.items()}


from pyqpanda import measure_all
def pyqpanda_measure(q, c):
    from pyqpanda import Measure
    return Measure(q, c)
