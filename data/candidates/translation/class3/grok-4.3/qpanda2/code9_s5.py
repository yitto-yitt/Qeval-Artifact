# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_efficientSU2():
    circuit = QCircuit()
    # rotation layer 0
    for i in range(3):
        circuit << RY(q[i], 0.0) << RZ(q[i], 0.0)
    circuit << BARRIER(q)
    # entanglement layer (reverse_linear)
    circuit << CNOT(q[2], q[1]) << CNOT(q[1], q[0])
    circuit << BARRIER(q)
    # rotation layer 1
    for i in range(3):
        circuit << RY(q[i], 0.0) << RZ(q[i], 0.0)
    return circuit

machine.finalize()
