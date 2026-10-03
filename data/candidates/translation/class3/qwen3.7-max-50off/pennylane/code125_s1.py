# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml

def circ_to_gate(circ):
    mat = qml.matrix(circ, wire_order=circ.wires)
    return qml.QubitUnitary(mat, wires=circ.wires)
