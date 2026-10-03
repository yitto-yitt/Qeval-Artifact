# EVAL_META: task_id=13, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QuantumMachine, QProg, U

def custom_rotation_gate():
    qm = QuantumMachine()
    q = qm.qAlloc(1)
    prog = QProg()
    prog << U(q[0], np.pi / 2, np.pi / 2, np.pi / 2)
    return prog
