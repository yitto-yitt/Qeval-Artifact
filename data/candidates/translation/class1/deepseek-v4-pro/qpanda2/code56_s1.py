# EVAL_META: task_id=56, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def not_gate(a):
    qvm = CPUQVM()
    qvm.init()
    q = qvm.qAlloc_many(8)
    c = qvm.cAlloc_many(8)
    prog = QProg()
    a_str = format(a, "08b")
    for i in range(8):
        if a_str[7 - i] == "0":
            prog << X(q[i])
    for i in range(8):
        prog << Measure(q[i], c[i])
    c_reversed = [c[7 - i] for i in range(8)]
    counts = qvm.run_with_configuration(prog, c_reversed, 1024)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
