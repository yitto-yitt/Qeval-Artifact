# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, RX

def create_parametrized_gate(theta=None):
    if theta is None:
        from sympy import Symbol
        theta = Symbol("theta")
    circuit = QCircuit(1)
    circuit << RX(0, theta)
    return circuit
