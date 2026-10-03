# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    circ_gate = qml.QubitUnitary(qml.matrix(circ), wires=circ.wires)
    return circ_gate
