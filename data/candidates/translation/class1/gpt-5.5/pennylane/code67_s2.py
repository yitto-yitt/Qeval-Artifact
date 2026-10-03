# EVAL_META: task_id=67, framework=pennylane, class=1
from numpy import pi
import pennylane as qml


def chsh_circuit(alice, bob):
    ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
    ]

    if alice == 0:
        ops.append(qml.RY(0, wires=0))
    else:
        ops.append(qml.RY(-pi / 2, wires=0))

    if bob == 0:
        ops.append(qml.RY(-pi / 4, wires=1))
    else:
        ops.append(qml.RY(pi / 4, wires=1))

    measurements = [qml.sample(wires=0), qml.sample(wires=1)]
    return qml.tape.QuantumScript(ops, measurements)
