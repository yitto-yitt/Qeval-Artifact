# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    matrix = qml.matrix(circ, wire_order=circ.wires)
    circ_gate = qml.QubitUnitary(matrix, wires=circ.wires)
    return circ_gate


# ==================================================
