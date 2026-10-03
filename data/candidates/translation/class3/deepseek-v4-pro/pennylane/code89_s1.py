# EVAL_META: task_id=89, framework=pennylane, class=3
import pennylane as qml

def create_controlled_hgate():
    """Construct a three-qubit controlled-Hadamard circuit (controls: 0,1; target: 2)."""
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit():
        qml.ctrl(qml.Hadamard(wires=2), control=[0, 1])
        return qml.state()
    return circuit
