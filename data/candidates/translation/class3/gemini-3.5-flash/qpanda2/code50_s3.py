# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()

def remove_gate_in_position(circuit, position):
    it = circuit.begin()
    for _ in range(position):
        it = it.get_next()
    circuit.delete_node(it)
    return circuit

machine.finalize()
