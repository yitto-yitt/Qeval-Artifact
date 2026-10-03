# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import *


def create_state_prep():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    prog = QProg()
    prog.insert(X(qubits[1]))
    
    return prog
