# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml

def create_diagonal_circuit(diag):
    n_qubits = qml.math.shape(diag)[0]
    n_qubits = int(qml.numpy.log2(n_qubits))
    dev = qml.device("default.qubit", wires=n_qubits)

    @qml.qnode(dev)
    def circuit():
        qml.DiagonalQubitUnitary(diag, wires=range(n_qubits))
        return qml.state()

    return circuit
