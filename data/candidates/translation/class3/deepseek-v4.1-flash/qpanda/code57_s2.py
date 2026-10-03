# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT

def create_swap_gate():
    circuit = QCircuit()
    circuit << CNOT(0, 1)
    circuit << CNOT(1, 0)
    circuit << CNOT(0, 1)
    return circuit
