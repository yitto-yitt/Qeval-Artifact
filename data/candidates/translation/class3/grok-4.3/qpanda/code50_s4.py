# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QProg

def remove_gate_in_position(circuit, position):
    new_prog = QProg()
    for i, gate in enumerate(circuit):
        if i != position:
            new_prog.insert(gate)
    return new_prog
