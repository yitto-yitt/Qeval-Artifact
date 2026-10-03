# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QProg

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "data"):
        del circuit.data[position]
        return circuit
    if isinstance(circuit, QProg):
        nodes = list(circuit)
        del nodes[position]
        new_prog = QProg()
        for node in nodes:
            new_prog << node
        return new_prog
    raise TypeError("Unsupported circuit type for remove_gate_in_position")
