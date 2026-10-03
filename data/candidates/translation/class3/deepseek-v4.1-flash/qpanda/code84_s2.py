# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, qAlloc, U3

def controlled_custom_unitary_circuit():
    q = qAlloc(2)
    circ = QCircuit()
    gate = U3(q[1], 0.3, 0.2, 0.1)
    controlled_gate = gate.control(q[0])
    circ << controlled_gate
    return circ
