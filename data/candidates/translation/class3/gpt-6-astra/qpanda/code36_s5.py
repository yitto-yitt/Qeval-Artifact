# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, I

def bv_function(s):
    n = len(s)
    qc = QCircuit()
    for qubit in range(n + 1):
        qc << I(qubit)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc << CNOT(index, n)
    return qc
