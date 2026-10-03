# EVAL_META: task_id=69, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    prog = QProg()
    prog << H(q[0]) << S(q[1]).control(q[0]) << H(q[1]) << S_dagger(q[0]).control(q[1])
    return prog

machine.finalize()
