# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import *

def apply_op_back():
    machine = CPUQVM()
    machine.initQVM()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    prog = QProg()
    circ = QCircuit()
    circ << H(q[0]) << CNOT(q[0], q[1])
    prog << circ
    prog << H(q[0])
    return prog
