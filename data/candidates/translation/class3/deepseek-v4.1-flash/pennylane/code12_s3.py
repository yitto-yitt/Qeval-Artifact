# EVAL_META: task_id=12, framework=pennylane, class=3
import pennylane as qml

def get_unitary():
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
    return qml.matrix(circuit, wire_order=[1, 0])()
