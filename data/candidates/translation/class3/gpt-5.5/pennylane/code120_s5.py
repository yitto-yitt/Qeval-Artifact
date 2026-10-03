# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml


def create_diagonal_circuit(diag):
    num_qubits = (len(diag) - 1).bit_length()
    op = qml.DiagonalQubitUnitary(diag, wires=range(num_qubits))
    return qml.tape.QuantumScript([op])
