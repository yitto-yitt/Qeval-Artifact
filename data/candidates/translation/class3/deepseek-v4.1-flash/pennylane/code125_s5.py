# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def circ_to_gate(circ):
    mat = qml.matrix(circ)
    if callable(mat):
        mat = mat()
    n = int(np.log2(mat.shape[0]))
    return qml.QubitUnitary(mat, wires=range(n))
