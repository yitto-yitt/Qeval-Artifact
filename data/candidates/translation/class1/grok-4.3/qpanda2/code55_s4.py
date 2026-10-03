# EVAL_META: task_id=55, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def or_gate(a, b):
    qvm = CPUQVM()
    qvm.initQVM()
    qr_a = qvm.qAllocMany(3)
    qr_b = qvm.qAllocMany(3)
    ancillary = qvm.qAllocMany(3)
    c = qvm.cAllocMany(3)
    prog = QProg()
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    for i in range(3):
        if a_str[2-i] == '0':
            prog.insert(X(qr_a[i]))
        if b_str[2-i] == '0':
            prog.insert(X(qr_b[i]))
    for i in range(3):
        prog.insert(Toffoli(qr_a[i], qr_b[i], ancillary[i]))
    for i in range(3):
        prog.insert(X(ancillary[i]))
    for i in range(3):
        prog.insert(Measure(ancillary[i], c[i]))
    shots = 1024
    counts = qvm.run_with_configuration(prog, shots, c)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
