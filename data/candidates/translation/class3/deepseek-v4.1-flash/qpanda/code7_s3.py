# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, RX, Parameter

def create_parametrized_gate():
    theta = Parameter("theta")
    circuit = QCircuit()
    qubit = Qubit(0)
    circuit << RX(qubit, theta)
    return circuit
