# EVAL_META: task_id=23, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def dj_constant_oracle():
    oracle = pq.QCircuit()
    oracle << pq.X(q[2])
    return oracle

def _cleanup():
    machine.finalize()

atexit.register(_cleanup)
