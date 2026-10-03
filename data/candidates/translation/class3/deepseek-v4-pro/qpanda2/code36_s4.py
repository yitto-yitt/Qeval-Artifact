# EVAL_META: task_id=36, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()

def bv_function(s):
    n = len(s)
    q = machine.qAlloc_many(n + 1)
    oracle = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            oracle << CNOT(q[index], q[n])
    return oracle

machine.finalize()
