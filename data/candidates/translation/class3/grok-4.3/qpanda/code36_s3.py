# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, CNOT

def bv_function(s):
    n = len(s)
    qc = QCircuit()
    qs = [Qubit(i) for i in range(n + 1)]
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc << CNOT(qs[index], qs[n])
    return qc
