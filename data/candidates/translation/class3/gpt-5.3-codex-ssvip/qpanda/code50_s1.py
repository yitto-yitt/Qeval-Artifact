# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_gate_in_position(circuit, position):
    if not isinstance(circuit, QCircuit):
        raise TypeError("circuit must be a QCircuit")
    circuit.remove_gate(position)
    return circuit
