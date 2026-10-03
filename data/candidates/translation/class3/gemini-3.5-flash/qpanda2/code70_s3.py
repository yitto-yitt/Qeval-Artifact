# EVAL_META: task_id=70, framework=qpanda2, class=3
from pyqpanda import *

# Initialize global QVM
machine = CPUQVM()
machine.init_qvm()
qlist = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    prog = QProg()
    prog << H(qlist[0])
    prog << CSWAP(qlist[0], qlist[1], qlist[2])
    prog << H(qlist[1])
    prog << S(qlist[0]).dagger().control([qlist[1]])
    return prog

# Manual Cleanup
machine.finalize()
