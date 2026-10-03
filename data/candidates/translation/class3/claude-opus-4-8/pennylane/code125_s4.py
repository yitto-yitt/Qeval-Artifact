# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def circ_to_gate(circ):
    wires = list(circ.wires)
    matrix = qml.matrix(circ, wire_order=wires)
    return qml.QubitUnitary(np.array(matrix), wires=wires)
