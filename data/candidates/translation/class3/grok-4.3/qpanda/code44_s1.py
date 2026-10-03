# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, X, CRY

def tensor_circuits():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    circ = QCircuit()
    circ << CRY(q[0], q[1], 0.2)
    circ << X(q[2])
    return circ
