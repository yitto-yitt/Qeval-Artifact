# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate, QVec

def create_cy_gate():
    q = QVec(2)
    circ = QCircuit()
    circ << QGate.sdg(q[1])
    circ << QGate.cx(q[0], q[1])
    circ << QGate.s(q[1])
    return circ
