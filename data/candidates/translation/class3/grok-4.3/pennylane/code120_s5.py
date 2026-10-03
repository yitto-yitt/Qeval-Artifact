# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml

def create_diagonal_circuit(diag):
    num_qubits = int(len(diag).bit_length() - 1)
    op = qml.DiagonalQubitUnitary(diag, wires=range(num_qubits))
    return qml.QuantumScript([op])
