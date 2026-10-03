# EVAL_META: task_id=13, framework=qpanda2, class=3
from pyqpanda import *
import math

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def custom_rotation_gate():
    q = qubits[0]
    prog = QProg()
    prog << U3(q, math.pi / 2, math.pi / 2, math.pi / 2)
    return prog

machine.finalize()
