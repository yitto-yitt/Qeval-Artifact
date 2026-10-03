# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml

def create_diagonal_circuit(diag):
    n_qubits = int(qml.math.log2(len(diag)))
    op = qml.DiagonalQubitUnitary(diag, wires=range(n_qubits))
    return qml.tape.QuantumScript([op])
