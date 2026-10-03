# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, 'data'):
        del circuit.data[position]
    else:
        del circuit[position]
    return circuit
