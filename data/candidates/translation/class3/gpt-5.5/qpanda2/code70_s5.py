# EVAL_META: task_id=70, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    prog = QProg()
    prog << H(q[0])
    prog << SWAP(q[1], q[2]).control([q[0]])
    prog << H(q[1])
    prog << S(q[0]).dagger().control([q[1]])
    return prog

atexit.register(machine.finalize)
