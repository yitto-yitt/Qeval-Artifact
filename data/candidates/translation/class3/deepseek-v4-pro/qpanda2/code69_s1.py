# EVAL_META: task_id=69, framework=qpanda2, class=3
import math
from pyqpanda import CPUQVM, QProg, H, CP

machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    prog = QProg()
    prog << H(q[0]) << CP(q[0], q[1], math.pi / 2) << H(q[1]) << CP(q[1], q[0], -math.pi / 2)
    return prog

machine.finalize()
