# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X

def bv_function(s):
    n = len(s)
    qc = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.insert(X(index).control([n]))
    return qc
