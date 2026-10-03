# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml
import numpy as np

def get_statevector(circuit):
    def _as_list(wires):
        if wires is None:
            return []
        try:
            return list(wires)
        except TypeError:
            return [wires]

    def _infer_wires(ops):
        inferred = []
        for op in ops:
            for w in _as_list(getattr(op, "wires", None)):
                if w not in inferred:
                    inferred.append(w)
        return inferred

    def _state_from_ops(ops, wires=None):
        ops = list(ops)
        wire_list = _as_list(wires)
        if not wire_list:
            wire_list = _infer_wires(ops)

        if not wire_list:
            return np.array([1.0 + 0.0j], dtype=complex)

        dev = qml.device("default.qubit", wires=wire_list)

        @qml.qnode(dev)
        def _runner():
            for op in ops:
                if getattr(op, "name", None) in {"Barrier", "WireCut"}:
                    continue
                qml.apply(op)
            return qml.state()

        return _runner()

    if isinstance(circuit, qml.QNode):
        tape = getattr(circuit, "_tape", None) or getattr(circuit, "qtape", None) or getattr(circuit, "tape", None)
        if tape is None:
            tape = circuit.construct((), {})
        return _state_from_ops(getattr(tape, "operations", []), circuit.device.wires)

    if hasattr(circuit, "operations"):
        wires = getattr(circuit, "wires", None)
        if (wires is None or len(_as_list(wires)) == 0) and hasattr(circuit, "num_wires"):
            wires = range(circuit.num_wires)
        return _state_from_ops(circuit.operations, wires)

    if isinstance(circuit, (list, tuple)):
        return _state_from_ops(circuit)

    if callable(circuit):
        with qml.queuing.AnnotatedQueue() as queue:
            result = circuit()
        tape = qml.tape.QuantumScript.from_queue(queue)
        if len(tape.operations) == 0 and not hasattr(result, "return_type"):
            return result
        return _state_from_ops(tape.operations, tape.wires)

    return np.asarray(circuit, dtype=complex)
