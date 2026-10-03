# EVAL_META: task_id=145, framework=pennylane, class=3
import pennylane as qml

def qft_inverse(n):
    ops = [qml.adjoint(qml.QFT(wires=range(n)))]
    return qml.QuantumScript(ops)
