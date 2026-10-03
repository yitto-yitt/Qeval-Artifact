# EVAL_META: task_id=53, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def xor_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    prog = QProg()
    xor_val = a ^ b
    for i in range(8):
        if (xor_val & (1 << i)) != 0:
            prog << X(qubits[i])
    prog << measure_all(qubits, cbits)
    shots = 1024
    result = qvm.run_with_configuration(prog, shots)
    counts = result
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
