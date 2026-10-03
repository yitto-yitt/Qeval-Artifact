# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml

def circ_to_gate(circ):
    U = qml.matrix(circ)
    if callable(U):
        U = U()
    return qml.QubitUnitary(U, wires=circ.wires)
