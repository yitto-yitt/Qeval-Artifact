# EVAL_META: task_id=24, framework=pennylane, class=1
import math
import numpy as np
import pennylane as qml


def dj_algorithm(oracle):
    def _oracle_wires(obj):
        if hasattr(obj, "wires"):
            try:
                ws = list(obj.wires)
                if len(ws) > 0:
                    return ws
            except Exception:
                pass
        return None

    wires = _oracle_wires(oracle)

    if wires is None:
        if hasattr(oracle, "num_qubits"):
            n = int(oracle.num_qubits)
        elif hasattr(oracle, "num_wires") and not isinstance(getattr(oracle, "num_wires"), property):
            n = int(oracle.num_wires)
        elif hasattr(oracle, "operations"):
            used = []
            for op in oracle.operations:
                used.extend(list(op.wires))
            wires = sorted(set(used))
            n = len(wires)
        else:
            arr = np.asarray(oracle)
            if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
                n = int(round(math.log2(arr.shape[0])))
            else:
                raise ValueError("Cannot determine the number of oracle qubits.")
        if wires is None:
            wires = list(range(n))
    else:
        n = len(wires)

    input_wires = wires[:-1]
    output_wire = wires[-1]

    def _apply_oracle():
        if isinstance(oracle, qml.operation.Operator):
            qml.apply(oracle)
            return

        if hasattr(oracle, "operations"):
            for op in oracle.operations:
                qml.apply(op)
            return

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

        if hasattr(oracle, "to_matrix"):
            qml.QubitUnitary(oracle.to_matrix(), wires=wires)
            return

        qml.QubitUnitary(np.asarray(oracle), wires=wires)

    dev = qml.device("default.qubit", wires=wires)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=output_wire)
        for w in wires:
            qml.Hadamard(wires=w)
        _apply_oracle()
        for w in wires:
            qml.Hadamard(wires=w)
        return qml.probs(wires=input_wires)

    probs = np.asarray(circuit(), dtype=float)
    m = len(input_wires)
    dist = {}

    for idx, prob in enumerate(probs):
        p = float(prob)
        if p > 1e-12:
            bits = format(idx, f"0{m}b") if m else ""
            dist[bits[::-1]] = p

    total = sum(dist.values())
    if total != 0.0:
        dist = {key: value / total for key, value in dist.items()}

    return dist
