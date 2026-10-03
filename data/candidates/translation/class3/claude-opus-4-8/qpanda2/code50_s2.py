# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()

def remove_gate_in_position(circuit, position):
    del circuit[position]
    return circuit

machine.finalize()
