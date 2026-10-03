# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_diagonal_circuit(diag):
    num_qubits = int(np.log2(len(diag)))
    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit():
        qml.DiagonalQubitUnitary(diag, wires=range(num_qubits))
        return qml.state()

    return circuit
