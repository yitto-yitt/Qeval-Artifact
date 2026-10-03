# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import *

def rx_gate(value=None):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    cbits = qvm.cAlloc_many(1)
    
    theta = var("theta")
    prog = QProg()
    prog.insert(RX(qubits[0], theta))
    
    if value is not None:
        prog = eval(prog, {theta: value})
        
    return prog
