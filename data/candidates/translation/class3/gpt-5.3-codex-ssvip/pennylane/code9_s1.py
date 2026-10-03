# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml


def create_efficientSU2():
    num_qubits = 3
    reps = 1
    wires = list(range(num_qubits))
    ops = []

    for _ in range(reps):
        for w in wires:
            ops.append(qml.RY(0.0, wires=w))
            ops.append(qml.RZ(0.0, wires=w))
        for i in range(num_qubits - 1):
            ops.append(qml.CNOT(wires=[i, i + 1]))
        for w in wires:
            ops.append(qml.Barrier(wires=[w]))

    for w in wires:
        ops.append(qml.RY(0.0, wires=w))
        ops.append(qml.RZ(0.0, wires=w))

    return qml.tape.QuantumTape(ops=ops, measurements=[])
