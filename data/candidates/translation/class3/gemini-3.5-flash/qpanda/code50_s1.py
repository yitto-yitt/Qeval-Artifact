# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def remove_gate_in_position(circuit: QuantumCircuit, position: int) -> QuantumCircuit:
    for attr in ['gates', '_gates', 'gate_list', '_gate_list', 'instructions', '_instructions', 'data']:
        if hasattr(circuit, attr):
            lst = getattr(circuit, attr)
            if isinstance(lst, list):
                del lst[position]
                break
    return circuit
