# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT

def inv_circuit(n):
    qc = QCircuit()
    for i in range(2):
        qc << H(i + 1)
    for i in range(2):
        qc << CNOT(i + 1, i + 3)
    return qc.dagger()
