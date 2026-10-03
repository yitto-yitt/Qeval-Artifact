# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    mat = qml.matrix(circ)
    n_wires = int(qml.math.log2(mat.shape[0]))
    circ_gate = qml.QubitUnitary(mat, wires=range(n_wires))
    return circ_gate
