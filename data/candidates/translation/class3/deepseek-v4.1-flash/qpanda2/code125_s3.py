# EVAL_META: task_id=125, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)

def circ_to_gate(circ):
    return circuit_to_gate(circ)

machine.finalize()
