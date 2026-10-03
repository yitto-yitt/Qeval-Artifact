# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    with qml.QueuingManager.stop_recording():
        if isinstance(circ, qml.QNode):
            tape = circ.construct((), {})
        elif isinstance(circ, qml.tape.QuantumScript):
            tape = circ
        elif isinstance(circ, qml.operation.Operator):
            tape = qml.tape.QuantumScript([circ])
        elif callable(circ):
            tape = qml.tape.make_qscript(circ)()
        else:
            tape = qml.tape.QuantumScript(list(circ))

        if tape.measurements:
            raise ValueError("A circuit containing measurements cannot become a gate.")

        for op in tape.operations:
            if isinstance(op, qml.operation.Channel) or not op.has_matrix:
                raise ValueError(
                    f"Operation {op.name} cannot be converted to a unitary gate."
                )

        wires = tape.wires
        matrix = qml.matrix(tape, wire_order=wires)

    return qml.QubitUnitary(matrix, wires=wires)
