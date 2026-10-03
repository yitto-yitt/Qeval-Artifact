# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import *
import pyqpanda3.core as pq

def create_parametrized_gate():
    theta = pq.Parameter("theta")
    qvm = pq.QVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    prog = pq.QProg()
    prog.insert(pq.RX(q[0], theta))
    return prog, theta
