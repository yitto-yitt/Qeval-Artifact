# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, H, CNOT

def simple_elitzur_vaidman():
    machine = CPUQVM()
    machine.initQVM()
    qvec = machine.qAlloc_many(2)
    prog = QProg()
    prog << H(qvec[0]) << CNOT(qvec[0], qvec[1]) << H(qvec[0])
    return prog
