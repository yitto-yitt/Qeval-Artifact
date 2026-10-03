# EVAL_META: task_id=53, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def xor_gate(a, b):
    init_quantum_machine(QMachineType.CPU)
    q = qAlloc_many(8)
    c = cAlloc_many(8)

    prog = QProg()

    x = a ^ b
    for i in range(8):
        if (x >> i) & 1:
            prog << X(q[i])

    for i in range(8):
        prog << Measure(q[i], c[i])

    shots = 1024
    counts = run_with_configuration(prog, c, shots)
    finalize()

    total = builtins.sum(counts.values())
    return {k: v / total for k, v in counts.items()}
