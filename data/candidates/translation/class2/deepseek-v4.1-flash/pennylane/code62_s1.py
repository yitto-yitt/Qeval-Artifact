# EVAL_META: task_id=62, framework=pennylane, class=2
import pennylane as qml


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)

    def circuit():
        for i in range(len(basis)):
            if state[i] == 1:
                qml.PauliX(wires=i)
            if basis[i] == 1:
                qml.Hadamard(wires=i)
        return [qml.state()]

    return qml.QNode(circuit, qml.device("default.qubit", wires=num_qubits))
