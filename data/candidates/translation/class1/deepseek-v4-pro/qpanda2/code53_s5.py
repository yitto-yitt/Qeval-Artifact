# EVAL_META: task_id=53, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def xor_gate(a, b):
    init(QMachineType.CPU)
    q = qAlloc_many(8)
    prog = QProg()

    for i in range(8):
        if (a >> i) & 1:
            prog << X(q[i])

    for i in range(8):
        if (b >> i) & 1:
            prog << X(q[i])

    result = prob_run_dict(prog, q[::-1])
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
