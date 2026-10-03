# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml


def create_diagonal_circuit(diag):
    num_qubits = len(diag).bit_length() - 1
    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit():
        qml.DiagonalQubitUnitary(diag, wires=range(num_qubits))
        return qml.state()

    return circuit
