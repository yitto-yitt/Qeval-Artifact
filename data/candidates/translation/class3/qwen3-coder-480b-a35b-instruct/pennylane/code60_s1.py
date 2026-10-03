# EVAL_META: task_id=60, framework=pennylane, class=3
import pennylane as qml

def create_cy_gate():
    def cy_gate(wires):
        qml.adjoint(qml.S)(wires=wires[1])
        qml.CNOT(wires=wires)
        qml.S(wires=wires[1])
    return cy_gate
