# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    n = int(np.log2(diag.size))
    if 2**n != diag.size:
        raise ValueError("Length of 'diag' must be a power of 2.")
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.DiagonalQubitUnitary(diag, wires=range(n))
        return qml.state()

    return circuit
