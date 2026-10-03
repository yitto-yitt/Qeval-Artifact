# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml

def create_diagonal_circuit(diag):
    num_qubits = len(diag).bit_length() - 1
    wires = list(range(num_qubits))
    with qml.tape.QuantumTape() as tape:
        qml.DiagonalQubitUnitary(diag, wires=wires)
    return tape
