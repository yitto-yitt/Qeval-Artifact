# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def circ_to_gate(circ):
    if isinstance(circ, qml.QNode):
        circ = circ.construct([], {})

    if callable(circ) and not hasattr(circ, "operations") and not isinstance(circ, qml.operation.Operator):
        circ = qml.tape.make_qscript(circ)()

    if isinstance(circ, qml.operation.Operator):
        wires = list(circ.wires)
        mat = qml.matrix(circ, wire_order=wires)
        return qml.QubitUnitary(mat, wires=wires)

    if hasattr(circ, "operations"):
        ops = list(circ.operations)
        wires = list(circ.wires)
    elif isinstance(circ, (list, tuple)):
        ops = list(circ)
        wires = []
        for op in ops:
            if hasattr(op, "wires"):
                for w in op.wires:
                    if w not in wires:
                        wires.append(w)
    else:
        mat = qml.matrix(circ)
        n = int(round(np.log2(np.shape(mat)[0])))
        wires = list(range(n))
        return qml.QubitUnitary(mat, wires=wires)

    n_wires = len(wires)
    if n_wires == 0:
        return qml.GlobalPhase(0.0, wires=[])

    dim = 2**n_wires
    unitary = np.eye(dim, dtype=complex)

    for op in ops:
        try:
            op_mat = qml.matrix(op, wire_order=wires)
        except Exception:
            if getattr(op, "name", None) == "Barrier":
                continue
            raise

        op_mat = qml.math.asarray(op_mat)
        if qml.math.shape(op_mat) == ():
            unitary = op_mat * unitary
        else:
            unitary = qml.math.matmul(op_mat, unitary)

    phase = getattr(circ, "global_phase", 0)
    if phase is not None and qml.math.allclose(phase, 0) is False:
        unitary = qml.math.exp(1j * phase) * unitary

    return qml.QubitUnitary(unitary, wires=wires)
