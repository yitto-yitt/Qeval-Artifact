# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    wires = circ.wires
    matrix = qml.matrix(circ, wire_order=wires)
    return qml.QubitUnitary(matrix, wires=wires)
