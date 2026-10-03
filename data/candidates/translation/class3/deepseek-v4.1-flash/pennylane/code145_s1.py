# EVAL_META: task_id=145, framework=pennylane, class=3
import pennylane as qml

def qft_inverse(n):
    return qml.QFT(wires=range(n)).adjoint()
