# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, Y

_qvm = CPUQVM()
try:
    _qvm.init()
except AttributeError:
    _qvm.init_qvm()

_q = _qvm.qAlloc_many(5)

def mcy(qc):
    qc << Y(_q[4]).control([_q[0], _q[1], _q[2], _q[3]])
    return qc
