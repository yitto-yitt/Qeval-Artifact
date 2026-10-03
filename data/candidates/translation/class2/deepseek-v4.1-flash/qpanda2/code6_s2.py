# EVAL_META: task_id=6, framework=qpanda2, class=2
from pyqpanda import QCircuit, X

def create_state_prep(num_qubits):
    qc = QCircuit()
    qc << X(0)
    return qc
