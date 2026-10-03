# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import *

def tensor_circuits():
    qvm = CPUQVM()
    qvm.init_qvm()
    top = QCircuit()
    q_top = qvm.qAlloc_many(1)
    top << X(q_top[0])
    bottom = QCircuit()
    q_bot = qvm.qAlloc_many(2)
    bottom << CRY(q_bot[0], q_bot[1], 0.2)
    tensored = QCircuit()
    tensored << bottom << top
    return tensored
