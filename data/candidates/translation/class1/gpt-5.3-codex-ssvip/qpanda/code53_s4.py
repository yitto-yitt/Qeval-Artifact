# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import *

def xor_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)

    prog = QProg()

    x = (a ^ b) & 0xFF
    for i in range(8):
        if (x >> i) & 1:
            prog << X(qubits[i])

    for i in range(8):
        prog << Measure(qubits[i], cbits[i])

    result = qvm.run_with_configuration(prog, cbits, 1024)
    qvm.finalize()

    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
