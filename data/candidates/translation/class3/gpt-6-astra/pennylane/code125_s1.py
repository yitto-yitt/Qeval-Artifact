# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    if circ.measurements:
        raise ValueError("A circuit with measurements cannot be converted into a gate.")
    return qml.QubitUnitary(
        qml.matrix(circ, wire_order=circ.wires),
        wires=circ.wires,
    )
