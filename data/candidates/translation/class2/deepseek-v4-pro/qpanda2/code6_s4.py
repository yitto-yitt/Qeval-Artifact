# EVAL_META: task_id=6, framework=qpanda2, class=2
from pyqpanda import *


def create_state_prep(num_qubits):
    q = qAlloc_many(num_qubits)
    circuit = QCircuit()
    circuit << X(q[0])
    return circuit
