# EVAL_META: task_id=41, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def compose_op():
    prog = QProg()
    prog << Y(qubits[0]) << X(qubits[2])
    return machine.get_unitary(prog)

machine.finalize()
