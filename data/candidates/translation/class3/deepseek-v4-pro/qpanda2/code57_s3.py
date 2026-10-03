# EVAL_META: task_id=57, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QProg, CNOT

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_swap_gate():
    prog = QProg()
    prog << CNOT(q[0], q[1]) << CNOT(q[1], q[0]) << CNOT(q[0], q[1])
    return prog

machine.finalize()
