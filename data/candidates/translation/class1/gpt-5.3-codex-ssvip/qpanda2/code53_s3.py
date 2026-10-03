# EVAL_META: task_id=53, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def xor_gate(a, b):
    shots = 1024
    init_quantum_machine(QMachineType.CPU)
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(8)
    c = qvm.cAlloc_many(8)

    prog = QProg()

    x = a ^ b
    for i in range(8):
        if (x >> i) & 1:
            prog << X(q[i])

    for i in range(8):
        prog << Measure(q[i], c[i])

    counts = qvm.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    qvm.finalize()
    destroy_quantum_machine(qvm)

    return {k: v / total for k, v in counts.items()}
