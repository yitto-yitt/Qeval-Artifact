# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def circ_to_gate(circ):
    def _as_wires(wires):
        if wires is None:
            return qml.wires.Wires([])
        return qml.wires.Wires(wires)

    def _ops_wire_order(ops):
        ordered = []
        for op in ops:
            for wire in op.wires:
                if wire not in ordered:
                    ordered.append(wire)
        return qml.wires.Wires(ordered)

    def _wire_order(obj, ops=None):
        try:
            wires = _as_wires(getattr(obj, "wires", None))
            if len(wires) > 0:
                return wires
        except Exception:
            pass

        if ops is not None:
            wires = _ops_wire_order(ops)
            if len(wires) > 0:
                return wires

        try:
            num_wires = int(getattr(obj, "num_wires"))
            if num_wires > 0:
                return qml.wires.Wires(range(num_wires))
        except Exception:
            pass

        return qml.wires.Wires([])

    def _matrix_from_ops(ops, wires):
        ops = list(ops)
        try:
            tape = qml.tape.QuantumScript(ops=ops, measurements=[])
            return qml.matrix(tape, wire_order=wires)
        except Exception:
            dim = 2 ** len(wires)
            mat = np.eye(dim, dtype=complex)
            for op in ops:
                mat = qml.math.matmul(qml.matrix(op, wire_order=wires), mat)
            return mat

    def _make_gate(mat, wires):
        if len(wires) == 0:
            shape = qml.math.shape(mat)
            if len(shape) >= 2 and int(shape[0]) > 1:
                num_wires = int(round(np.log2(int(shape[0]))))
                wires = qml.wires.Wires(range(num_wires))
        return qml.QubitUnitary(mat, wires=wires)

    if hasattr(circ, "operations"):
        ops = list(circ.operations)
        wires = _wire_order(circ, ops)
        mat = _matrix_from_ops(ops, wires)
        return _make_gate(mat, wires)

    if isinstance(circ, (list, tuple)):
        ops = list(circ)
        wires = _ops_wire_order(ops)
        mat = _matrix_from_ops(ops, wires)
        return _make_gate(mat, wires)

    if isinstance(circ, qml.operation.Operator):
        wires = _wire_order(circ, [circ])
        mat = qml.matrix(circ, wire_order=wires)
        return _make_gate(mat, wires)

    if callable(circ):
        try:
            tape = qml.tape.make_qscript(circ)()
            ops = list(tape.operations)
            wires = _wire_order(tape, ops)
            mat = _matrix_from_ops(ops, wires)
            return _make_gate(mat, wires)
        except Exception:
            pass

        try:
            device = getattr(circ, "device", None)
            wires = _as_wires(getattr(device, "wires", None))
            if len(wires) > 0:
                mat = qml.matrix(circ, wire_order=wires)()
            else:
                mat = qml.matrix(circ)()
            return _make_gate(mat, wires)
        except Exception:
            pass

    wires = _wire_order(circ)
    try:
        mat = qml.matrix(circ, wire_order=wires)
    except Exception:
        mat = qml.matrix(circ)

    if callable(mat):
        mat = mat()

    return _make_gate(mat, wires)
