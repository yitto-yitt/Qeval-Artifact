# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import *

def circuit():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    cbits = qvm.cAlloc_many(1)
    
    theta = var(0.0)
    
    prog = QProg()
    prog.insert(single_gate_apply_to_all(H, qubits))
    prog.insert(RZ(qubits[0], theta))
    
    return prog, qubits, cbits, qvm, theta
