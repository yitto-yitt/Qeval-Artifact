# EVAL_META: task_id=39, framework=pennylane, class=2
import pennylane as qml

def create_uniform_superposition(n):
    dev = qml.device("default.qubit", wires=n)
    @qml.qnode(dev)
    def circuit():
        qml.broadcast(qml.Hadamard, wires=range(n), pattern="single")
        return qml.state()
    return circuit()
