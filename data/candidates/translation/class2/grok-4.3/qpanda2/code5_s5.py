# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import *
def create_state_prep():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    cir = QCircuit()
    cir << X(q[0])
    return cir
