# EVAL_META: task_id=54, framework=qpanda2, class=1
import builtins
from pyqpanda import *
def and_gate(a, b):
    a = format(a, '03b')
    b = format(b, '03b')
    init(QMachineType.CPU)
    q_a = qAlloc_many(3)
    q_b = qAlloc_many(3)
    ancillary = qAlloc_many(3)
    cbits = cAlloc_many(3)
    prog = QProg()
    for i in range(3):
        if a[2-i] == '1':
            prog << X(q_a[i])
        if b[2-i] == '1':
            prog << X(q_b[i])
    for i in range(3):
        prog << Toffoli(q_a[i], q_b[i], ancillary[i])
    for i in range(3):
        prog << Measure(ancillary[i], cbits[i])
    shots = 1024
    result = run_with_configuration(prog, shots)
    counts = result
    total = builtins.sum(counts.values())
    finalize()
    return {key: value / total for key, value in counts.items()}
