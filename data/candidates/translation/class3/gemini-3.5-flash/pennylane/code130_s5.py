# EVAL_META: task_id=130, framework=pennylane, class=3
import pennylane as qml

def inv_circuit(n):
    def circuit():
        for i in range(2):
            qml.Hadamard(wires=i+1)
        for i in range(2):
            qml.CNOT(wires=[i+1, i+3])
    return qml.adjoint(circuit)
