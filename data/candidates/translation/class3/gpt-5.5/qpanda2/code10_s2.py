# EVAL_META: task_id=10, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
c = machine.cAlloc_many(2)

def create_operator():
    circ = QCircuit()
    circ << X(q[0]) << X(q[1])
    return circ

atexit.register(machine.finalize)
