# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_diagonal_circuit(diag):
    diag_arr = np.asarray(diag, dtype=complex)
    n = int(np.log2(diag_arr.size))
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.DiagonalQubitUnitary(diag_arr, wires=range(n))
        return qml.state()

    return circuit
