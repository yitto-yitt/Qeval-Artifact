# EVAL_META: task_id=38, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    prog = QProg()
    prog << H(q[0])
    prog << CRZ(q[0], q[1], theta)
    prog << H(q[1])
    prog << CRY(q[1], q[0], theta)
    return prog

atexit.register(machine.finalize)
