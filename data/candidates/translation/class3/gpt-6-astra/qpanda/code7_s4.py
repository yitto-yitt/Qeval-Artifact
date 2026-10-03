# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Parameter, RX

def create_parametrized_gate():
    theta = Parameter("theta")
    quantum_circuit = QCircuit()
    quantum_circuit << RX(0, theta)
    return quantum_circuit
