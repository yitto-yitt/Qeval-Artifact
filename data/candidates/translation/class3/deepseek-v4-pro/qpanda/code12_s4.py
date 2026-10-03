# EVAL_META: task_id=12, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit


def get_unitary():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc.get_matrix()
