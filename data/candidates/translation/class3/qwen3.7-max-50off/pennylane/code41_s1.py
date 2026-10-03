# EVAL_META: task_id=41, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def compose_op():
    op = qml.PauliX(0) @ qml.PauliY(2)
    mat = qml.matrix(op, wire_order=[0, 1, 2])
    return qml.Hermitian(mat, wires=[0, 1, 2])
