# EVAL_META: task_id=69, framework=qpanda2, class=3
import math
from pyqpanda import *

init(QMachineType.CPU)
q = qAlloc_many(2)

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    prog = QProg()
    prog << H(q[0])
    prog << U1(q[0], math.pi / 4.0)
    prog << U1(q[1], math.pi / 4.0)
    prog << CNOT(q[0], q[1])
    prog << U1(q[1], -math.pi / 4.0)
    prog << CNOT(q[0], q[1])
    prog << H(q[1])
    prog << U1(q[1], -math.pi / 4.0)
    prog << U1(q[0], -math.pi / 4.0)
    prog << CNOT(q[1], q[0])
    prog << U1(q[0], math.pi / 4.0)
    prog << CNOT(q[1], q[0])
    return prog

finalize()
