# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml

def circ_to_gate(circ):
    wires = circ.wires
    mat = qml.matrix(circ)
    circ_gate = qml.QubitUnitary(mat, wires=wires)
    return circ_gate
