# EVAL_META: task_id=3, framework=pennylane, class=2
import pennylane as qml


def create_ghz(drawing=False):
    ghz = qml.tape.QuantumScript(
        ops=[
            qml.Hadamard(wires=0),
            qml.CNOT(wires=[0, 1]),
            qml.CNOT(wires=[0, 2]),
        ],
        measurements=[qml.sample(wires=[0, 1, 2])],
    )
    if drawing:
        fig, _ = qml.drawer.tape_mpl(ghz)
        return ghz, fig
    return ghz
