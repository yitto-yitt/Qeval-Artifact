# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_gate_in_position(circuit, position):
    new_circuit = QCircuit()
    for i, gate in enumerate(circuit.data):
        if i != position:
            new_circuit << gate
    return new_circuit
