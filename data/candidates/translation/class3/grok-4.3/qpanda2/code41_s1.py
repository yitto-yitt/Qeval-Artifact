# EVAL_META: task_id=41, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def compose_op():
    circuit = QCircuit()
    circuit << X(q[0]) << Y(q[2])
    prog = QProg()
    prog << circuit
    op = get_unitary_matrix(prog)
    return op

machine.finalize()
