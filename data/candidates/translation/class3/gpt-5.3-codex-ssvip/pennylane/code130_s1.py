# EVAL_META: task_id=130, framework=pennylane, class=3
import pennylane as qml

def inv_circuit(n):
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        for i in range(2):
            qml.Hadamard(wires=i + 1)
        for i in range(2):
            qml.CNOT(wires=[i + 1, i + 3])
        return qml.state()

    inv_ops = [qml.adjoint(op) for op in reversed(circuit.tape.operations)]

    @qml.qnode(dev)
    def inverse_circuit():
        for op in inv_ops:
            qml.apply(op)
        return qml.state()

    return inverse_circuit
