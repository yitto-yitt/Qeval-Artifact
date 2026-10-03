# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    if hasattr(circ, "operations"):
        ops = circ.operations
    else:
        ops = circ

    if not ops:
        wires = getattr(circ, "wires", [0])
        return qml.Identity(wires=wires)

    return qml.prod(*ops)
