# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def tensor_circuits():
    circ = QuantumCircuit(3)
    circ.cry(0, 1, 0.2)
    circ.x(2)
    return circ
