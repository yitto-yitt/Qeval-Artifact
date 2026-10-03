# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml
from sympy import symbols


def create_efficientSU2():
    parameters = symbols("theta_0:12", real=True)

    with qml.tape.QuantumTape() as circuit:
        for wire in range(3):
            qml.RY(parameters[wire], wires=wire)
        for wire in range(3):
            qml.RZ(parameters[3 + wire], wires=wire)

        qml.Barrier(wires=range(3))
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[0, 1])
        qml.Barrier(wires=range(3))

        for wire in range(3):
            qml.RY(parameters[6 + wire], wires=wire)
        for wire in range(3):
            qml.RZ(parameters[9 + wire], wires=wire)

    return circuit
