# EVAL_META: task_id=89, framework=qpanda2, class=3
from pyqpanda import *

init(QMachineType.CPU)
qvm = CPUQVM()
qvm.init()
q = qvm.qAlloc_many(3)

def create_controlled_hgate():
    cir = QCircuit()
    cir << H(q[2]).control([q[0], q[1]])
    return cir

qvm.finalize()
