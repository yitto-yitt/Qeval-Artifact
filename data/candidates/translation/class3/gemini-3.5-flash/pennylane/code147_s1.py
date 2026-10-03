# EVAL_META: task_id=147, framework=pennylane, class=3
import pennylane as qml

def mcy(qc):
    op = qml.ctrl(qml.PauliY(4), control=[0, 1, 2, 3])
    qc.append(op)
    return qc
