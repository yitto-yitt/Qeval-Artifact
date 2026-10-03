# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml
import math

def create_diagonal_circuit(diag):
    num_qubits = int(math.log2(len(diag)))
    return qml.DiagonalQubitUnitary(diag, wires=range(num_qubits))
