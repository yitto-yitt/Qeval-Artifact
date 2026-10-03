# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    if callable(circ):
        unitary = qml.matrix(circ)()
        wires = circ.wires
    else:
        unitary = qml.matrix(circ)
        wires = circ.wires
    return qml.QubitUnitary(unitary, wires=wires)
