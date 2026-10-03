# EVAL_META: task_id=59, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QProg, H, CNOT

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_cz_gate():
    prog = QProg()
    prog << H(q[1]) << CNOT(q[0], q[1]) << H(q[1])
    return prog

machine.finalize()
