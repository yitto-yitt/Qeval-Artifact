# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H, CNOT

def apply_op_back():
    q = [Qubit(i) for i in range(3)]
    circ = QCircuit()
    circ << H(q[0])
    circ << CNOT(q[0], q[1])
    circ << H(q[0])
    return circ
