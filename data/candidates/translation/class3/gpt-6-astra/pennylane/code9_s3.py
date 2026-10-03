# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np


def create_efficientSU2():
    num_qubits = 3
    reps = 1
    parameters = np.zeros(2 * num_qubits * (reps + 1), requires_grad=True)
    wires = range(num_qubits)

    with qml.tape.QuantumTape() as circuit:
        index = 0
        for layer in range(reps + 1):
            for rotation in (qml.RY, qml.RZ):
                for wire in wires:
                    rotation(parameters[index], wires=wire)
                    index += 1

            if layer < reps:
                qml.Barrier(wires=wires)
                for wire in reversed(range(num_qubits - 1)):
                    qml.CNOT(wires=[wire, wire + 1])
                qml.Barrier(wires=wires)

    return circuit
