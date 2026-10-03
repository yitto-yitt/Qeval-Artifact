# EVAL_META: task_id=145, framework=pennylane, class=3
import pennylane as qml

def qft_inverse(n):
    qft_op = qml.QFT(wires=list(range(n)))
    return qml.adjoint(qft_op)
