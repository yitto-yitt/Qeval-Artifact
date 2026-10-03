# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import *

def bv_function(s):
    n = len(s)
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(n + 1)
    prog = QProg()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(q[index], q[n])
    return prog
