# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    qml.draw(circ)
    unitary = qml.matrix(circ)()
    num_wires = len(circ.wires) if hasattr(circ, 'wires') else circ.num_wires
    return qml.QubitUnitary(unitary, wires=range(num_wires))
