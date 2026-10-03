# EVAL_META: task_id=3, framework=pennylane, class=2
import pennylane as qml


def create_ghz(drawing=False):
    ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
        qml.CNOT(wires=[0, 2]),
    ]
    measurements = [qml.probs(wires=[0, 1, 2])]
    ghz = qml.tape.QuantumScript(ops, measurements)

    if drawing:
        fig, _ = qml.draw_mpl(ghz)
        return ghz, fig

    return ghz
