# EVAL_META: task_id=52, framework=pennylane, class=1
import pennylane as qml


def send_bits(bitstring):
    operations = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
    ]

    if bitstring[1] == "1":
        operations.append(qml.PauliZ(wires=0))
    if bitstring[0] == "1":
        operations.append(qml.PauliX(wires=0))

    operations.extend(
        [
            qml.CNOT(wires=[0, 1]),
            qml.Hadamard(wires=0),
        ]
    )

    measurements = [qml.sample(wires=[1, 0])]
    return qml.tape.QuantumScript(operations, measurements, shots=1)
