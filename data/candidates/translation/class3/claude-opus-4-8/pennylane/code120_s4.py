# EVAL_META: task_id=120, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    num_qubits = int(np.log2(len(diag)))
    wires = list(range(num_qubits))

    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit():
        qml.DiagonalQubitUnitary(diag, wires=wires)
        return qml.state()

    return circuit
