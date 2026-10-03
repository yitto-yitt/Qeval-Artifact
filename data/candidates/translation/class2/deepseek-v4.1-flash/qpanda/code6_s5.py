# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, X


def create_state_prep(num_qubits):
    cir = QCircuit()
    cir << X(0)
    return cir
