# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, RX, var

def create_parametrized_gate():
    theta = var("theta")
    circuit = QCircuit()
    circuit << RX(0, theta)
    return circuit
