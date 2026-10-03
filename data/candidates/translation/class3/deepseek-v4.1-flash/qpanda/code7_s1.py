# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, RX, Var

def create_parametrized_gate():
    theta = Var("theta")
    q = Qubit(0)
    circuit = QCircuit()
    circuit << RX(q, theta)
    return circuit
