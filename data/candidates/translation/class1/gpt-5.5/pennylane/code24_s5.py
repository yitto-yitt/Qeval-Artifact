# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def dj_algorithm(oracle):
    n = getattr(oracle, "num_qubits", None)
    if callable(n):
        n = n()
    if n is None:
        owires = getattr(oracle, "wires", None)
        if owires is not None:
            n = len(owires)
    if n is None:
        n = getattr(oracle, "num_wires", None)
        if callable(n):
            n = n()
    if n is None or not isinstance(n, int):
        ops = getattr(oracle, "operations", None)
        if ops:
            all_wires = []
            for op in ops:
                all_wires.extend(list(op.wires))
            n = len(dict.fromkeys(all_wires))
    n = int(n)

    wires = list(range(n))
    input_wires = list(range(n - 1))

    def apply_oracle():
        if isinstance(oracle, qml.operation.Operator):
            op_wires = list(oracle.wires)
            if op_wires != wires and len(op_wires) == n:
                qml.apply(qml.map_wires(oracle, {op_wires[i]: wires[i] for i in range(n)}))
            else:
                qml.apply(oracle)
            return

        ops = getattr(oracle, "operations", None)
        if ops is not None and all(isinstance(op, qml.operation.Operator) for op in ops):
            old_wires = []
            for op in ops:
                for w in op.wires:
                    if w not in old_wires:
                        old_wires.append(w)
            wire_map = {old_wires[i]: wires[i] for i in range(min(len(old_wires), n))}
            for op in ops:
                qml.apply(qml.map_wires(op, wire_map) if wire_map else op)
            return

        if oracle.__class__.__module__.startswith("qiskit") and hasattr(qml, "from_qiskit"):
            try:
                qml.from_qiskit(oracle)(wires=wires)
                return
            except Exception:
                pass

        if callable(oracle):
            try:
                oracle(wires=wires)
                return
            except TypeError:
                pass
            try:
                oracle(wires)
                return
            except TypeError:
                pass
            oracle()
            return

        try:
            mat = qml.matrix(oracle)
            qml.QubitUnitary(mat, wires=wires)
            return
        except Exception:
            pass

        try:
            from qiskit.quantum_info import Operator
            mat = Operator(oracle).data
            dim = 2 ** n
            perm = np.array([int(format(i, "0{}b".format(n))[::-1], 2) for i in range(dim)])
            mat = mat[np.ix_(perm, perm)]
            qml.QubitUnitary(mat, wires=wires)
            return
        except Exception as exc:
            raise TypeError("Unsupported oracle type for PennyLane translation") from exc

    dev = qml.device("default.qubit", wires=wires)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n - 1)
        for w in wires:
            qml.Hadamard(wires=w)
        apply_oracle()
        for w in wires:
            qml.Hadamard(wires=w)
        return qml.probs(wires=input_wires)

    if n - 1 == 0:
        return {"": 1.0}

    probs = np.asarray(circuit(), dtype=float)
    result = {}
    m = n - 1
    for i, p in enumerate(probs):
        if p > 1e-12:
            result[format(i, "0{}b".format(m))[::-1]] = float(p)

    total = sum(result.values())
    if total:
        result = {k: v / total for k, v in result.items()}
    return result
