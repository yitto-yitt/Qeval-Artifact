# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    dev = qml.device("default.qubit", wires=circuit.num_wires if hasattr(circuit, "num_wires") else None)

    @qml.qnode(dev)
    def _circuit():
        circuit()
        return qml.state()

    return _circuit()
