# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    wires = circ.wires
    mat = qml.matrix(circ, wire_order=wires)
    if callable(mat):
        mat = mat()
    return qml.QubitUnitary(mat, wires=wires, do_queue=False)
