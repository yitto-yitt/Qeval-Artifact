# EVAL_META: task_id=3, framework=pennylane, class=2
import pennylane as qml
import matplotlib.pyplot as plt


def create_ghz(drawing=False):
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[0, 2])
        return qml.counts()

    if drawing:
        # Draw the circuit using matplotlib
        qml.drawer.use_style("black_white")
        fig, ax = qml.draw_mpl(circuit)()
        return circuit, fig
    return circuit
