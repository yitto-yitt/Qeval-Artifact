# EVAL_META: task_id=55, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def or_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    qr_a = machine.qAlloc_many(3)
    qr_b = machine.qAlloc_many(3)
    ancillary = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    prog = QProg()
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    for i in range(3):
        if a_str[2-i] == '0':
            prog << X(qr_a[i])
        if b_str[2-i] == '0':
            prog << X(qr_b[i])
    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])
    for i in range(3):
        prog << X(ancillary[i])
    for i in range(3):
        prog << Measure(ancillary[i], cbits[i])
    shots = 1024
    counts = machine.run_with_configuration(prog, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
