# EVAL_META: task_id=109, framework=pennylane, class=3
import pennylane as qml

def circuit():
    def ansatz(theta):
        qml.Hadamard(wires=0)
        qml.RZ(theta, wires=0)
    return ansatz
