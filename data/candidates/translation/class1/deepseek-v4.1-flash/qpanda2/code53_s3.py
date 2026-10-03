# EVAL_META: task_id=53, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def xor_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(8)
    c = machine.cAlloc_many(8)
    prog = QProg()
    result = a ^ b
    for i in range(8):
        if (result >> i) & 1:
            prog << X(q[i])
    for i in range(8):
        prog << measure(q[i], c[7 - i])
    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    machine.finalize()
    return {key: value / total for key, value in counts.items()}
