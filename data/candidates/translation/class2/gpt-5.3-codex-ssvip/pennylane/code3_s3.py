# EVAL_META: task_id=3, framework=pennylane, class=2
import pennylane as qml


def create_ghz(drawing=False):
    tape = qml.tape.QuantumTape()
    with tape:
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[0, 2])
        qml.sample(wires=[0, 1, 2])
    if drawing:
        drawer = qml.draw(tape)
        return tape, drawer
    return tape
