# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, CCX, Measure

def and_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    qr_a = machine.qAlloc_many(3)
    qr_b = machine.qAlloc_many(3)
    ancillary = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    prog = QProg()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    for i in range(3):
        if a_bin[2 - i] == '1':
            prog << X(qr_a[i])
        if b_bin[2 - i] == '1':
            prog << X(qr_b[i])
    for i in range(3):
        prog << CCX(qr_a[i], qr_b[i], ancillary[i])
    for i in range(3):
        prog << Measure(ancillary[i], cbits[i])
    result = machine.run_with_configuration(prog, cbits, shots=1024)
    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
