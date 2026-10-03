# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, CNOT

def bv_function(s):
    n = len(s)
    qc = QCircuit()
    ancilla = Qubit(n)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc << CNOT(Qubit(index), ancilla)
    return qc
