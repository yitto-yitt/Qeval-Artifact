# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, I

def bv_function(s):
    n = len(s)
    circuit = QCircuit()
    for qubit in range(n + 1):
        circuit << I(qubit)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit << CNOT(index, n)
    return circuit
