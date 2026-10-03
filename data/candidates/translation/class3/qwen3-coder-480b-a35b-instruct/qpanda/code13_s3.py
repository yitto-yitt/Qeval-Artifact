# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def custom_rotation_gate():
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc()
    prog = QProg()
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2
    prog.insert(RX(q, theta)).insert(RZ(q, phi + lam)).insert(RX(q, -theta)).insert(RZ(q, 0))
    # Actually implementing U gate as RZ(phi)*RX(theta)*RZ(lambda) decomposition
    prog.clear()
    prog.insert(U3(q, theta, phi, lam))
    return prog
