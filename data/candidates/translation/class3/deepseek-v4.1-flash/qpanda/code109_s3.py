# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H, RZ, var

def circuit():
    q = Qubit(0)
    qc = QCircuit()
    qc << H(q)
    qc << RZ(q, var(0))
    return qc
