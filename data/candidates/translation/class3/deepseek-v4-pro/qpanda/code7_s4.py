# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, var

def create_parametrized_gate():
    theta = var("theta")
    circuit = QuantumCircuit(1)
    circuit.rx(0, theta)
    return circuit
