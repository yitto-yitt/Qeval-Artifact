# EVAL_META: task_id=8, framework=qpanda, class=3
import pyqpanda3 as pq
from pyqpanda3.core import *

def rx_gate(value=None):
    theta = pq.QProg()
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    
    if value is not None:
        prog = pq.QProg()
        prog.insert(pq.RX(q[0], value))
        qvm.finalize()
        return prog
    else:
        # In pyQPanda3, we create a parameterized gate when value is None
        prog = pq.QProg()
        # We'll use a symbolic approach for parameterized gates
        # Since pyQPanda3 doesn't have direct parameter support like Qiskit,
        # we return a program that can be modified later
        prog.insert(pq.RX(q[0], 0.0))  # placeholder
        qvm.finalize()
        return prog
