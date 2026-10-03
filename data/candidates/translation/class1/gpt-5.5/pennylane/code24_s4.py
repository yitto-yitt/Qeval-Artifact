# EVAL_META: task_id=24, framework=pennylane, class=1
import numpy as np
import pennylane as qml

def dj_algorithm(oracle):
    def _matrix_qubits(obj):
        shape = np.shape(obj)
        if len(shape) == 2 and shape[0] == shape[1] and shape[0] > 0:
            dim = shape[0]
            n_qubits = int(np.log2(dim))
            if 2 ** n_qubits == dim:
                return n_qubits
        return None

    def _ordered_union_wires(ops):
        wires = []
        for op in ops:
            if hasattr(op, "wires"):
                for w in qml.wires.Wires(op.wires):
                    if w not in wires:
                        wires.append(w)
        return wires

    n = None
    wire_order = None

    if hasattr(oracle, "num_qubits"):
        try:
            n = int(oracle.num_qubits)
        except Exception:
            n = None

    if n is None and hasattr(oracle, "wires"):
        try:
            wire_order = list(qml.wires.Wires(oracle.wires))
            if len(wire_order) > 0:
                n = len(wire_order)
        except Exception:
            wire_order = None

    if n is None and hasattr(oracle, "num_wires"):
        try:
            n = int(oracle.num_wires)
        except Exception:
            n = None

    if n is None and isinstance(oracle, (list, tuple)):
        wire_order = _ordered_union_wires(oracle)
        if len(wire_order) > 0:
            n = len(wire_order)

    if n is None:
        n = _matrix_qubits(oracle)

    if n is None:
        raise ValueError("Unable to determine the number of oracle qubits.")

    if wire_order is None:
        wire_order = list(range(n))

    input_wires = wire_order[:-1]
    output_wire = wire_order[-1]
    measured_wires = list(reversed(input_wires))

    dev = qml.device("default.qubit", wires=wire_order)

    def _apply_oracle():
        qiskit_like = hasattr(oracle, "num_qubits") and not hasattr(oracle, "wires")

        if qiskit_like:
            try:
                from qiskit.quantum_info import Operator as QiskitOperator
                mat = np.asarray(QiskitOperator(oracle).data, dtype=complex)
                qml.QubitUnitary(mat, wires=list(reversed(wire_order)))
                return
            except Exception:
                pass

            try:
                mat = np.asarray(oracle.to_matrix(), dtype=complex)
                qml.QubitUnitary(mat, wires=list(reversed(wire_order)))
                return
            except Exception:
                pass

            try:
                qfunc = qml.from_qiskit(oracle)
                qfunc(wires=wire_order)
                return
            except Exception:
                pass

        if isinstance(oracle, (list, tuple)):
            for op in oracle:
                qml.apply(op)
            return

        if hasattr(oracle, "operations"):
            for op in oracle.operations:
                qml.apply(op)
            return

        if isinstance(oracle, qml.operation.Operator):
            qml.apply(oracle)
            return

        if callable(oracle):
            try:
                oracle(wires=wire_order)
                return
            except TypeError:
                pass
            try:
                oracle(wire_order)
                return
            except TypeError:
                pass
            oracle()
            return

        try:
            mat = np.asarray(oracle, dtype=complex)
            qml.QubitUnitary(mat, wires=wire_order)
            return
        except Exception:
            pass

        try:
            mat = qml.matrix(oracle, wire_order=wire_order)
            qml.QubitUnitary(mat, wires=wire_order)
            return
        except Exception as exc:
            raise ValueError("Unable to apply oracle.") from exc

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=output_wire)
        for w in wire_order:
            qml.Hadamard(wires=w)
        _apply_oracle()
        for w in wire_order:
            qml.Hadamard(wires=w)
        if len(measured_wires) == 0:
            return qml.probs(wires=[output_wire])
        return qml.probs(wires=measured_wires)

    probs = np.asarray(circuit(), dtype=float)

    if len(measured_wires) == 0:
        return {"": 1.0}

    result = {}
    width = len(measured_wires)
    for i, p in enumerate(probs):
        if p > 1e-12:
            result[format(i, f"0{width}b")] = float(p)

    return result
