# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, X


def create_state_prep(num_qubits):
    qc = QCircuit()
    if num_qubits > 0:
        qc << X(0)
    return qc
