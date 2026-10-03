# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml

def create_diagonal_circuit(diag):
    n_qubits = len(diag).bit_length() - 1
    wires = list(range(n_qubits))
    op = qml.DiagonalQubitUnitary(diag, wires=wires)
    return qml.tape.QuantumScript([op])
