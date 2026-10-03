# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import QuantumCircuit


def create_state_prep():
    qc = QuantumCircuit(2)
    qc.x(0)
    return qc
