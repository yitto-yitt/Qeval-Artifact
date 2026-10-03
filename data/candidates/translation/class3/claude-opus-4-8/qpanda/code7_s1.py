# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, RX

def create_parametrized_gate():
    theta = Parameter("theta")
    quantum_circuit = QCircuit(1)
    quantum_circuit << RX(0, theta.value)
    return quantum_circuit, theta


class Parameter:
    def __init__(self, name):
        self.name = name
        self.value = 0.0
