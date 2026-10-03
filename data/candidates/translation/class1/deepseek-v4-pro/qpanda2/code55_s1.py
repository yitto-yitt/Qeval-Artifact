# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def or_gate(a, b):
    init(QMachineType.CPU)
    qvm = CPUQVM()
    qvm.initQVM()

    qa = qvm.qAlloc_many(3)
    qb = qvm.qAlloc_many(3)
    qanc = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    prog = QProg()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')

    for i in range(3):
        if a_bin[2 - i] == '0':
            prog << X(qa[i])
        if b_bin[2 - i] == '0':
            prog << X(qb[i])

    for i in range(3):
        prog << Toffoli(qa[i], qb[i], qanc[i])

    for i in range(3):
        prog << X(qanc[i])

    for i in range(3):
        prog << Measure(qanc[i], cbits[i])

    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)
    qvm.finalize()

    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
