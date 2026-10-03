# EVAL_META: task_id=3, framework=pennylane, class=2
import pennylane as qml
import matplotlib.pyplot as plt


def create_ghz(drawing=False):
    dev = qml.device("default.qubit", wires=3, shots=1024)

    @qml.qnode(dev)
    def ghz():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[0, 2])
        return qml.sample()

    if drawing:
        fig, ax = qml.draw_mpl(ghz)()
        return ghz, fig
    return ghz
