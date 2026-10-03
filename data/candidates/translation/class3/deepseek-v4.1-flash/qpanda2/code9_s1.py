# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qv = machine.qAlloc_many(3)


def create_efficientSU2():
    angles = [0.1 * (i + 1) for i in range(12)]
    circuit = QCircuit()

    # Rep 0 rotation layer: RY on each qubit (reverse_linear entanglement default)
    for i in range(3):
        circuit << RY(qv[i], angles[i])
    # Rep 0 rotation layer: RZ on each qubit
    for i in range(3):
        circuit << RZ(qv[i], angles[3 + i])

    # Entanglement layer (reverse_linear for 3 qubits -> [1,2] then [0,1])
    circuit << CNOT(qv[1], qv[2])
    circuit << CNOT(qv[0], qv[1])

    # Rep 1 rotation layer: RY on each qubit
    for i in range(3):
        circuit << RY(qv[i], angles[6 + i])
    # Rep 1 rotation layer: RZ on each qubit
    for i in range(3):
        circuit << RZ(qv[i], angles[9 + i])

    return circuit


machine.finalize()
