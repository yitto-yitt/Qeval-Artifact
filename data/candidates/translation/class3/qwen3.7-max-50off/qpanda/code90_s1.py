# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, X, H

def create_custom_controlled():
    qc = QuantumCircuit(4)
    qc << X(1, [0, 3])
    qc << H(2, [0, 3])
    return qc
