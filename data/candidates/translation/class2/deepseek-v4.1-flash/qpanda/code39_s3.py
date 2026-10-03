# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, H, StateVector


def create_uniform_superposition(n):
    circuit = QCircuit()
    for i in range(n):
        circuit << H(i)
    return StateVector(circuit)
