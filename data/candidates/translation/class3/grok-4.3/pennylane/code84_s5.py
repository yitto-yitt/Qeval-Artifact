# EVAL_META: task_id=84, framework=pennylane, class=3
import pennylane as qml

def controlled_custom_unitary_circuit():
    custom_gate = qml.ctrl(qml.U3(0.3, 0.2, 0.1, wires=1), control=0)
    qc = qml.QuantumScript([custom_gate])
    return qc
