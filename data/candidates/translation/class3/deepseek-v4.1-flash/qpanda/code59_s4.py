# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT

def create_cz_gate():
    circuit = QCircuit()
    circuit << H(1)
    circuit << CNOT(0, 1)
    circuit << H(1)
    return circuit
