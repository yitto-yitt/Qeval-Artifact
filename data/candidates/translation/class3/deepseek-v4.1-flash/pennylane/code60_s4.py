# EVAL_META: task_id=60, framework=pennylane, class=3
import pennylane as qml

def create_cy_gate():
    def circuit():
        qml.adjoint(qml.S)(wires=1)
        qml.CNOT(wires=[0, 1])
        qml.S(wires=1)
    return circuit
