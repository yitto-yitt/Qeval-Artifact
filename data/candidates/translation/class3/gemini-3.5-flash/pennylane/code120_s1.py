# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_diagonal_circuit(diag):
    num_qubits = int(np.round(np.log2(len(diag))))
    def circuit():
        qml.DiagonalQubitUnitary(np.array(diag), wires=range(num_qubits))
    return circuit
