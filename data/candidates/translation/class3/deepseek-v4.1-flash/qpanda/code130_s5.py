# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT

def inv_circuit(n):
    qc = QCircuit(n)
    qc << CNOT(2, 4)
    qc << CNOT(1, 3)
    qc << H(2)
    qc << H(1)
    return qc
