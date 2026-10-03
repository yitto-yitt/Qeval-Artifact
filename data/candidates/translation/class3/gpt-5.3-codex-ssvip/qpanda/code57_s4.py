# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CX


def create_swap_gate():
    circuit = QCircuit()
    circuit << CX(0, 1)
    circuit << CX(1, 0)
    circuit << CX(0, 1)
    return circuit
