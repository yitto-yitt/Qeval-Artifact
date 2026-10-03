# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_gate_in_position(circuit, position):
    try:
        del circuit[position]
    except (TypeError, AttributeError):
        gates = circuit.get_gate_list()
        gate_to_remove = gates[position]
        circuit.remove_gate(gate_to_remove)
    return circuit
