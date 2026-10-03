# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import *


def create_state_prep(num_qubits):
    circuit = QCircuit()
    circuit << X(Qubit(0))
    return circuit
