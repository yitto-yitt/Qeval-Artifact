# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda import *

def dj_constant_oracle():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    
    prog = QProg()
    prog.insert(X(qubits[2]))
    
    return prog
