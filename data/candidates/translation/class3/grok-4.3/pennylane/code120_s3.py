# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml
import math

def create_diagonal_circuit(diag):
    num_qubits = int(math.log2(len(diag)))
    diagonal_op = qml.DiagonalQubitUnitary(diag, wires=range(num_qubits))
    qc = qml.tape.QuantumScript([diagonal_op])
    return qc
