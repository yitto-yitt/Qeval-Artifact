# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    if isinstance(circ, qml.QNode):
        tape = getattr(circ, "_tape", None)
        circ = tape if tape is not None else circ.construct((), {})
    elif isinstance(circ, (list, tuple)):
        circ = qml.tape.QuantumScript(circ)
    elif callable(circ) and not isinstance(circ, qml.operation.Operator):
        circ = qml.tape.make_qscript(circ)()

    wires = circ.wires
    matrix = qml.matrix(circ, wire_order=wires)
    return qml.QubitUnitary(matrix, wires=wires)
