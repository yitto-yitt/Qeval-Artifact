# EVAL_META: task_id=120, framework=pennylane, class=3
import math
import pennylane as qml


def create_diagonal_circuit(diag):
    num_qubits = int(math.log2(len(diag)))
    op = qml.DiagonalQubitUnitary(diag, wires=range(num_qubits))
    return qml.tape.QuantumScript([op], [])
