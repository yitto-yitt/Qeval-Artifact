# EVAL_META: task_id=3, framework=pennylane, class=2
import pennylane as qml


def create_ghz(drawing=False):
    dev = qml.device("default.qubit", wires=3, shots=1024)

    @qml.qnode(dev)
    def ghz():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[0, 2])
        return qml.sample(wires=[0, 1, 2])

    if drawing:
        drawing_obj = qml.draw_mpl(ghz)()
        return ghz, drawing_obj
    return ghz
