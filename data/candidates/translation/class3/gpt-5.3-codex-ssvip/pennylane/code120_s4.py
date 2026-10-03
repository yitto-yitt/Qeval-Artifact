# EVAL_META: task_id=120, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    n = int(np.log2(len(diag)))
    if 2**n != len(diag):
        raise ValueError("Length of 'diag' must be a power of 2.")
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.QubitUnitary(np.diag(diag), wires=range(n))
        return qml.state()

    return circuit
