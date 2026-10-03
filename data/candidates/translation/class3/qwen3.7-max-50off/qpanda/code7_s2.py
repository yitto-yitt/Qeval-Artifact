# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, Parameter

def create_parametrized_gate():
    theta = Parameter("theta")
    qc = QuantumCircuit(1)
    qc.rx(theta, 0)
    return qc
