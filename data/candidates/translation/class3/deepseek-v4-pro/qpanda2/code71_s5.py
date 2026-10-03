# EVAL_META: task_id=71, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_csx01_h1():
    prog = QProg()
    prog << H(q[0]) << CSX(q[0], q[1]) << H(q[1])
    return prog

machine.finalize()
