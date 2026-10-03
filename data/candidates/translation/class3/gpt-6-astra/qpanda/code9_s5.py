# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QProg, Parameter, RY, RZ, CNOT, BARRIER


def create_efficientSU2():
    theta = [Parameter(f"θ[{i}]") for i in range(12)]
    circuit = QProg()

    for qubit in range(3):
        circuit << RY(qubit, theta[qubit])
    for qubit in range(3):
        circuit << RZ(qubit, theta[3 + qubit])

    circuit << BARRIER([0, 1, 2])
    circuit << CNOT(1, 2)
    circuit << CNOT(0, 1)
    circuit << BARRIER([0, 1, 2])

    for qubit in range(3):
        circuit << RY(qubit, theta[6 + qubit])
    for qubit in range(3):
        circuit << RZ(qubit, theta[9 + qubit])

    return circuit
