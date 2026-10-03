# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    wires = getattr(circ, "wires", None)

    if wires is None:
        tape = qml.tape.make_qscript(circ)()
        wires = tape.wires
        mat = qml.matrix(tape, wire_order=wires)
    else:
        mat = qml.matrix(circ, wire_order=wires)

    return qml.QubitUnitary(mat, wires=wires)
