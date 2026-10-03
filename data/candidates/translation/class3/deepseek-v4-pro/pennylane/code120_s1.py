# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_diagonal_circuit(diag):
    n = len(diag)
    n_qubits = int(np.log2(n))
    mat = np.diag(diag)
    dev = qml.device('default.qubit', wires=n_qubits)
    
    @qml.qnode(dev)
    def circuit():
        qml.QubitUnitary(mat, wires=range(n_qubits))
        return qml.state()
    return circuit
