# EVAL_META: task_id=44, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def tensor_circuits():
    top = QCircuit()
    top.insert(X(q[2]))
    bottom = QCircuit()
    bottom.insert(CRY(q[0], q[1], 0.2))
    tensored = QCircuit()
    tensored.insert(bottom)
    tensored.insert(top)
    return tensored

machine.finalize()
