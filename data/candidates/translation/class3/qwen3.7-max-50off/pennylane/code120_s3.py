# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml
import math

def create_diagonal_circuit(diag):
    num_qubits = int(math.log2(len(diag)))
    with qml.tape.QuantumTape() as tape:
        qml.DiagonalQubitUnitary(diag, wires=list(range(num_qubits)))
    return tape
