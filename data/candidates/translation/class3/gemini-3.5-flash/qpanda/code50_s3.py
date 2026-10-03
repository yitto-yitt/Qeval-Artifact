# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QProg, QCircuit

def remove_gate_in_position(circuit, position):
    nodes = list(circuit)
    if position < 0:
        position += len(nodes)
    new_circuit = type(circuit)()
    for idx, node in enumerate(nodes):
        if idx != position:
            new_circuit << node
    return new_circuit
