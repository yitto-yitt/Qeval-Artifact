# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QVec, CBit, H, CNOT, Measure

def bell_dag():
    q = QVec(3)
    c = CBit(3)
    circ = QCircuit()
    circ << H(q[0])
    circ << CNOT(q[0], q[1])
    circ << Measure(q[0], c[0])
    return circ
