# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml

def create_diagonal_circuit(diag):
    diag_len = len(diag)
    if diag_len == 0 or (diag_len & (diag_len - 1)) != 0:
        raise ValueError("Input diagonal must have length equal to a power of 2.")
    num_qubits = diag_len.bit_length() - 1
    op = qml.DiagonalQubitUnitary(diag, wires=range(num_qubits))
    return qml.tape.QuantumScript([op])
