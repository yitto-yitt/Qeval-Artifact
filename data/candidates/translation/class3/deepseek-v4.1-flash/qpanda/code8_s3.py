# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, RX, Parameter

def rx_gate(value=None):
    theta = Parameter("theta")
    q = Qubit(0)
    circuit = QCircuit()
    circuit << RX(q, theta)
    if value is not None:
        circuit.assign_parameters({theta: value})
    return circuit
