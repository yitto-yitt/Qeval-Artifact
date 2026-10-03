# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import QMachine, QCircuit, Var, H, RZ

def circuit():
    qm = QMachine()
    q = qm.qAlloc_many(1)
    qc = QCircuit()
    qc << H(q[0])
    theta = Var('th')
    qc << RZ(q[0], theta)
    return qc
