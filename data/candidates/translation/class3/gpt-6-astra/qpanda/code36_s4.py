# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT

def bv_function(s):
    n = len(s)
    circuit = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit << CNOT(index, n)
    return circuit
