# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import Circuit, Parameter, RX

def create_parametrized_gate():
    theta = Parameter("theta")
    circuit = Circuit(1)
    circuit.append(RX(0, theta))
    return circuit
