# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def custom_rotation_gate():
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(1)
    prog = QProg()
    
    # U gate with theta=pi/2, phi=pi/2, lambda=pi/2
    prog << U(q[0], np.pi / 2, np.pi / 2, np.pi / 2)
    
    return prog
