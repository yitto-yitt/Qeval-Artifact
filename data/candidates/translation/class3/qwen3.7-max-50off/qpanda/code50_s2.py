# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, 'data'):
        del circuit.data[position]
    elif hasattr(circuit, 'pop'):
        circuit.pop(position)
    else:
        try:
            del circuit[position]
        except Exception:
            pass
    return circuit
