# EVAL_META: task_id=38, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    prog = QProg()
    prog << H(q[0]) \
         << RZ(q[1], theta / 2) \
         << CNOT(q[0], q[1]) \
         << RZ(q[1], -theta / 2) \
         << CNOT(q[0], q[1]) \
         << H(q[1]) \
         << RY(q[0], theta / 2) \
         << CNOT(q[1], q[0]) \
         << RY(q[0], -theta / 2) \
         << CNOT(q[1], q[0])
    return prog

machine.finalize()
