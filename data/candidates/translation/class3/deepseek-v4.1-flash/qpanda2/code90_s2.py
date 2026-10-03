# EVAL_META: task_id=90, framework=qpanda2, class=3
import math
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    circuit = QCircuit()
    circuit << Toffoli(q[0], q[3], q[1])
    circuit << H(q[2])
    circuit << Toffoli(q[0], q[3], q[2])
    circuit << H(q[2])
    circuit << Toffoli(q[0], q[3], q[2])
    circuit << RY(q[2], -math.pi / 4)
    circuit << Toffoli(q[0], q[3], q[2])
    circuit << RY(q[2], math.pi / 4)
    return circuit

machine.finalize()
