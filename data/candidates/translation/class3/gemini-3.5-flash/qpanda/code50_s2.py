# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import *

def remove_gate_in_position(circuit, position):
    nodes = list(circuit)
    circuit.clear()
    for i, node in enumerate(nodes):
        if i != position:
            circuit << node
    return circuit
