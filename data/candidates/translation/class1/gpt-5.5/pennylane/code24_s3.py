# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def dj_algorithm(oracle):
    wires = None

    if hasattr(oracle, "wires"):
        try:
            owires = list(oracle.wires)
            if len(owires) > 0:
                wires = owires
        except Exception:
            wires = None

    if hasattr(oracle, "num_qubits"):
        n = int(oracle.num_qubits)
        if wires is None or len(wires) != n:
            wires = list(range(n))
    elif wires is not None:
        n = len(wires)
    else:
        arr = np.asarray(oracle)
        n = int(round(np.log2(arr.shape[0])))
        wires = list(range(n))

    input_wires = wires[:-1]
    output_wire = wires[-1]
    dev = qml.device("default.qubit", wires=wires)

    def apply_item(item):
        if item is None:
            return
        if isinstance(item, qml.operation.Operator):
            qml.apply(item)
            return
        if hasattr(item, "operations"):
            for op in item.operations:
                apply_item(op)
            return
        if isinstance(item, (list, tuple)):
            for op in item:
                apply_item(op)
            return
        mat = np.asarray(item)
        if mat.ndim == 2:
            qml.QubitUnitary(mat, wires=wires)

    def apply_oracle():
        if isinstance(oracle, qml.operation.Operator):
            qml.apply(oracle)
            return
        if hasattr(oracle, "operations"):
            for op in oracle.operations:
                apply_item(op)
            return
        if isinstance(oracle, (list, tuple)):
            for op in oracle:
                apply_item(op)
            return
        if callable(oracle):
            try:
                oracle(wires=wires)
            except TypeError:
                try:
                    oracle(wires)
                except TypeError:
                    oracle()
            return
        try:
            qfunc = qml.from_qiskit(oracle)
            qfunc(wires=wires)
            return
        except Exception:
            pass
        qml.QubitUnitary(np.asarray(oracle), wires=wires)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=output_wire)
        for w in wires:
            qml.Hadamard(wires=w)
        apply_oracle()
        for w in wires:
            qml.Hadamard(wires=w)
        return qml.probs(wires=input_wires)

    probs = np.asarray(circuit(), dtype=float)
    m = n - 1
    result = {}

    for i, p in enumerate(probs):
        if p > 1e-12:
            bits = format(i, f"0{m}b") if m > 0 else ""
            result[bits[::-1]] = float(p)

    total = sum(result.values())
    if total != 0:
        result = {k: v / total for k, v in result.items()}

    return result
