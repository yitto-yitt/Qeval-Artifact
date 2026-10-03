# EVAL_META: task_id=147, framework=pennylane, class=3
import pennylane as qml

def mcy(qc):
    qc.append(qml.ctrl(qml.PauliY, control=[0, 1, 2, 3])(wires=4))
    return qc
