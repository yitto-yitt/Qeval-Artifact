# EVAL_META: task_id=147, framework=pennylane, class=3
import pennylane as qml

def mcy(qc):
    mcy_gate = qml.ctrl(qml.PauliY, control=[0, 1, 2, 3])
    qc.append(mcy_gate(wires=[4]))
    return qc
