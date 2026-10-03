# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import *

def simple_elitzur_vaidman():
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qAlloc_many(2)
    prog = QProg()
    
    prog << H(q[0]) << CNOT(q[0], q[1]) << H(q[0])
    
    return prog
