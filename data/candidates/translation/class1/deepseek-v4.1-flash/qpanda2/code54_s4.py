# EVAL_META: task_id=54, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def and_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    qr_a = machine.qAlloc_many(3)
    qr_b = machine.qAlloc_many(3)
    ancillary = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    prog = QProg()
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
        prog << Measure(ancillary[i], cbits[i])
    shots = 1024
    result = machine.run_with_configuration(prog, shots)
    machine.finalize()
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
