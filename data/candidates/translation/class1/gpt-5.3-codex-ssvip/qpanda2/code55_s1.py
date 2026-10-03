# EVAL_META: task_id=55, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def or_gate(a, b):
    init(QMachineType.CPU)
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(9)
    c = qvm.cAlloc_many(3)

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    prog = QProg()

    for i in range(3):
        if a_bits[2 - i] == '0':
            prog << X(q[i])
        if b_bits[2 - i] == '0':
            prog << X(q[3 + i])

    for i in range(3):
        prog << Toffoli(q[i], q[3 + i], q[6 + i])

    for i in range(3):
        prog << X(q[6 + i])

    for i in range(3):
        prog << Measure(q[6 + i], c[i])

    shots = 1000
    counts = qvm.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    result = {k: v / total for k, v in counts.items()}

    qvm.finalize()
    destroy_quantum_machine(qvm)
    return result
