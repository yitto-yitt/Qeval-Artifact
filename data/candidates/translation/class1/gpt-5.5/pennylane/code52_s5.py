# EVAL_META: task_id=52, framework=pennylane, class=1
import pennylane as qml


def send_bits(bitstring):
    sender = 0
    receiver = 1

    ops = [
        qml.Hadamard(wires=sender),
        qml.CNOT(wires=[sender, receiver]),
    ]

    if bitstring[1] == "1":
        ops.append(qml.PauliZ(wires=sender))
    if bitstring[0] == "1":
        ops.append(qml.PauliX(wires=sender))

    ops.extend(
        [
            qml.CNOT(wires=[sender, receiver]),
            qml.Hadamard(wires=sender),
        ]
    )

    measurements = [qml.sample(wires=[receiver, sender])]
    return qml.tape.QuantumScript(ops, measurements, shots=1)
