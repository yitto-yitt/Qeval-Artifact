# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def custom_rotation_gate():
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(1)
    prog = QProg()
    prog.insert(RX(q[0], np.pi / 2)).insert(RZ(q[0], np.pi / 2)).insert(RX(q[0], np.pi / 2))
    return prog
