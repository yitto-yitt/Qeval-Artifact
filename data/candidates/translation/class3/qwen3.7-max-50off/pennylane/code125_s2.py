# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml
import math

def circ_to_gate(circ):
    U = qml.matrix(circ)
    if hasattr(circ, 'wires'):
        wires = circ.wires
    else:
        n = int(math.log2(U.shape[0]))
        wires = list(range(n))
    return qml.QubitUnitary(U, wires=wires)
