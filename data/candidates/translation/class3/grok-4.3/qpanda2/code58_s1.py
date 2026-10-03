# EVAL_META: task_id=58, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
machine = CPUQVM()
machine.init_qvm()
q = qAlloc_many(2)
def create_ch_gate():
    circuit = create_empty_circuit()
    circuit << RY(q[1], np.pi/4) << CX(q[0], q[1]) << RY(q[1], -np.pi/4)
    return circuit
machine.finalize()
