# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import *

def xor_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)

    prog = QProg()

    x = a ^ b
    for i in range(8):
        if (x >> i) & 1:
            prog << X(qubits[i])

    for i in range(8):
        prog << Measure(qubits[i], cbits[i])

    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)

    qvm.finalize()

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
