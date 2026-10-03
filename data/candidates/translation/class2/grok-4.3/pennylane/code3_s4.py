# EVAL_META: task_id=3, framework=pennylane, class=2
import pennylane as qml


def create_ghz(drawing=False):
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def ghz_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[0, 2])
        return qml.counts()

    if drawing:
        fig, _ = qml.draw_mpl(ghz_circuit)()
        return ghz_circuit, fig
    return ghz_circuit
