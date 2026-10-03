# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3 import QCircuit

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, 'data'):
        del circuit.data[position]
        return circuit
        
    new_circuit = QCircuit()
    for i, node in enumerate(circuit):
        if i != position:
            new_circuit << node
    return new_circuit
