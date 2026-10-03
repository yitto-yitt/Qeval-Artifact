# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, 'data'):
        del circuit.data[position]
    elif hasattr(circuit, '__delitem__'):
        del circuit[position]
    return circuit
