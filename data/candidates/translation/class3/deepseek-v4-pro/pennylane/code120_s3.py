# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    wires = list(range(n))
    ops = [qml.DiagonalQubitUnitary(np.array(diag), wires=wires)]
    return qml.tape.QuantumScript(ops)
