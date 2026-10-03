# EVAL_META: task_id=12, framework=qpanda, class=3
from pyqpanda3 import QuantumCircuit

def get_unitary():
    circ = QuantumCircuit(2)
    circ.h(0)
    circ.cx(0, 1)
    return circ.to_matrix()
