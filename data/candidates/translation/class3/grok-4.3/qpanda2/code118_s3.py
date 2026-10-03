# EVAL_META: task_id=118, framework=qpanda2, class=3
from pyqpanda import *
import math
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)
def create_c3sx_circuit():
    circuit = QCircuit()
    sx_u3 = U3(q[3], math.pi/2, -math.pi/2, math.pi/2)
    circuit << sx_u3.control([q[0], q[1], q[2]])
    return circuit
machine.finalize()
