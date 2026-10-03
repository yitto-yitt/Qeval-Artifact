# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def bv_function(s):
    n = len(s)
    qc = QuantumCircuit(n + 1)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(index, n)
    return qc
