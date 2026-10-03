# EVAL_META: task_id=130, framework=pennylane, class=3
import pennylane as qml


def inv_circuit(n):
    with qml.tape.QuantumTape() as tape:
        for i in range(2):
            qml.Hadamard(wires=i + 1)
        for i in range(2):
            qml.CNOT(wires=[i + 1, i + 2 + 1])

    ops = [qml.adjoint(op) for op in reversed(tape.operations)]

    with qml.tape.QuantumTape() as inv_tape:
        for op in ops:
            qml.apply(op)

    return inv_tape
