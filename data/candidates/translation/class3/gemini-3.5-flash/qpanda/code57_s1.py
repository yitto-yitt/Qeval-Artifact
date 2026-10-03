# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, CNOT

def create_swap_gate():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = QProg()
    prog << CNOT(q[0], q[1]) << CNOT(q[1], q[0]) << CNOT(q[0], q[1])
    return prog
