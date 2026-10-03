# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)
def remove_gate_in_position(circuit, position):
    del circuit.data[position]
    return circuit
machine.finalize()
