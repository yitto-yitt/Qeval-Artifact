# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, qAlloc_many, CX

def bv_function(s):
    n = len(s)
    qc = QCircuit()
    q = qAlloc_many(n + 1)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc << CX(q[index], q[n])
    return qc
