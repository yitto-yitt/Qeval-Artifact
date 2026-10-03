# EVAL_META: task_id=125, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def circ_to_gate(circ):
    def _tape_from_circuit(c):
        if hasattr(c, "operations"):
            return c, None

        if isinstance(c, qml.QNode):
            tape = None
            try:
                tape = c.construct((), {})
            except Exception:
                tape = None
            if tape is None:
                tape = getattr(c, "_tape", None)
            if tape is None:
                tape = getattr(c, "qtape", None)
            return tape, c

        if callable(c):
            with qml.queuing.AnnotatedQueue() as queue:
                c()
            return qml.tape.QuantumScript.from_queue(queue), None

        return c, None

    tape, qnode = _tape_from_circuit(circ)

    if tape is None:
        raise ValueError("Unable to convert the provided circuit to a PennyLane gate.")

    operations = list(getattr(tape, "operations", []))

    if qnode is not None and hasattr(qnode, "device") and getattr(qnode.device, "wires", None) is not None:
        wires = qnode.device.wires
    else:
        wires = getattr(tape, "wires", qml.wires.Wires([]))

    wires = qml.wires.Wires(wires)
    num_wires = len(wires)

    total_matrix = None

    for op in operations:
        try:
            op_matrix = qml.matrix(op, wire_order=wires)
        except Exception:
            if getattr(op, "name", None) in {"Barrier", "Snapshot"}:
                continue
            raise

        if total_matrix is None:
            total_matrix = op_matrix
        else:
            total_matrix = qml.math.matmul(op_matrix, total_matrix)

    if total_matrix is None:
        total_matrix = np.eye(2**num_wires, dtype=complex)

    return qml.QubitUnitary(total_matrix, wires=wires, unitary_check=False)
