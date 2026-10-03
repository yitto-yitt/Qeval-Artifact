# EVAL_META: task_id=44, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def tensor_circuits():
    top = QCircuit()
    top << X(q[0])

    bottom = QCircuit()
    bottom << RY(q[2], 0.2).control([q[1]])

    tensored = QCircuit()
    tensored << bottom
    tensored << top
    return tensored

atexit.register(machine.finalize)
