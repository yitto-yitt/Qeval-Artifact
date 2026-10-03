# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import *

def w_state():
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    
    prog = QProg()
    prog.insert(RY(q[0], 2 * arccos(1 / sqrt(3))))
    prog.insert(CH(q[0], q[1]))
    prog.insert(CX(q[1], q[2]))
    prog.insert(CX(q[0], q[1]))
    prog.insert(X(q[0]))
    
    for i in range(3):
        prog.insert(Measure(q[i], c[i]))
    
    return prog
