# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_efficientSU2():
    circuit = QCircuit()

    for i in range(3):
        circuit << RY(q[i], 0.0)
        circuit << RZ(q[i], 0.0)

    circuit << CNOT(q[0], q[1])
    circuit << CNOT(q[0], q[2])
    circuit << CNOT(q[1], q[2])

    circuit << BARRIER(q)

    return circuit

machine.finalize()
