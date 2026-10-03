# EVAL_META: task_id=8, framework=qpanda, class=3
import pyqpanda3 as pq
from pyqpanda3.core import *

def rx_gate(value=None):
    theta = pq.Parameter("theta")
    qvm = pq.QVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    
    prog = pq.QProg()
    prog.insert(pq.RX(q[0], theta))
    
    if value is not None:
        # Substitute the parameter with the given value
        substituted_prog = pq.bind_parameters(prog, {theta: value})
        qvm.finalize()
        return substituted_prog
    else:
        qvm.finalize()
        return prog
