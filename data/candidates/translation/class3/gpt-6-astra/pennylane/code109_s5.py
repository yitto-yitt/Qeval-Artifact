# EVAL_META: task_id=109, framework=pennylane, class=3
import pennylane as qml

def circuit():
    dev = qml.device("default.qubit", wires=1)

    @qml.qnode(dev)
    def quantum_circuit(th):
        qml.Hadamard(wires=0)
        qml.RZ(th, wires=0)
        return qml.state()

    return quantum_circuit
