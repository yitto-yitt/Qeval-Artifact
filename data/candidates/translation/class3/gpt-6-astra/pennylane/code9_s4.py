# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml
from sympy import Symbol


def create_efficientSU2():
    parameters = [Symbol(f"θ[{i}]", real=True) for i in range(12)]
    operations = []

    for layer in range(2):
        offset = 6 * layer
        operations.extend(
            qml.RY(parameters[offset + wire], wires=wire)
            for wire in range(3)
        )
        operations.extend(
            qml.RZ(parameters[offset + 3 + wire], wires=wire)
            for wire in range(3)
        )

        if layer == 0:
            operations.append(qml.Barrier(wires=range(3)))
            operations.append(qml.CNOT(wires=[1, 2]))
            operations.append(qml.CNOT(wires=[0, 1]))
            operations.append(qml.Barrier(wires=range(3)))

    return qml.tape.QuantumScript(operations)
