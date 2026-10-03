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
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    for i in range(3):
        if a_str[2 - i] == '1':
            prog.insert(X(qr_a[i]))
        if b_str[2 - i] == '1':
            prog.insert(X(qr_b[i]))
    for i in range(3):
        prog.insert(CCX(qr_a[i], qr_b[i], ancillary[i]))
    for i in range(3):
        prog.insert(Measure(ancillary[i], cbits[i]))
    counts = machine.run_with_configuration(prog, cbits, 1024)
    total = sum(counts.values())
    machine.finalize()
    return {key: value / total for key, value in counts.items()}
