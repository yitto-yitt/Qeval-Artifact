# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)


def create_efficientSU2():
    circuit = QCircuit()
    thetas = [var("theta_%d" % i) for i in range(12)]

    # rotation layer 1: RY on all qubits, then RZ on all qubits
    for i in range(3):
        circuit << RY(q[i], thetas[i])
    for i in range(3):
        circuit << RZ(q[i], thetas[i + 3])

    circuit << BARRIER(q)

    # entanglement layer (full): CNOT on all pairs
    circuit << CNOT(q[0], q[1])
    circuit << CNOT(q[0], q[2])
    circuit << CNOT(q[1], q[2])

    circuit << BARRIER(q)

    # final rotation layer: RY on all qubits, then RZ on all qubits
    for i in range(3):
        circuit << RY(q[i], thetas[i + 6])
    for i in range(3):
        circuit << RZ(q[i], thetas[i + 9])

    return circuit


machine.finalize()
