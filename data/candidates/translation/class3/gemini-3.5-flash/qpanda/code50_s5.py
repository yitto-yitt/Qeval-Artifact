# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QProg, QCircuit

def remove_gate_in_position(circuit, position):
    new_circuit = type(circuit)()
    for i, node in enumerate(circuit):
        if i != position:
            new_circuit << node
    return new_circuit
