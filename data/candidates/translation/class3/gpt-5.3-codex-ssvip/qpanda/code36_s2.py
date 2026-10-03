# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import Circuit, X, control

def bv_function(s):
    n = len(s)
    qc = Circuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc << control(X(n), [index])
    return qc
