# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_operator():
    qc = QuantumCircuit(2, 2)
    qc.x(0)
    qc.x(1)
    return qc
