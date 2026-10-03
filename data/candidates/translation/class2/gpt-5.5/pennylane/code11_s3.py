# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml
import numpy as np

def get_statevector(circuit):
    def _wire_list(wires):
        if wires is None:
            return []
        try:
            return list(wires)
        except TypeError:
            try:
                return list(range(int(wires)))
            except Exception:
                return [wires]

    def _append_operation_wires(wires, operations):
        out = list(wires)
        for op in operations:
            for w in _wire_list(getattr(op, "wires", [])):
                if w not in out:
                    out.append(w)
        return out

    def _execute_operations(operations, wires):
        operations = list(operations)
        wires = _append_operation_wires(wires, operations)
        if not wires:
            return np.array([1.0 + 0.0j], dtype=complex)
        dev = qml.device("default.qubit", wires=wires)
        tape = qml.tape.QuantumScript(operations, [qml.state()], shots=None)
        return qml.execute([tape], dev)[0]

    if hasattr(circuit, "construct") and hasattr(circuit, "device"):
        tape = circuit.construct((), {})
        if tape is None and hasattr(circuit, "_tape"):
            tape = circuit._tape
        wires = _wire_list(getattr(circuit.device, "wires", None))
        if not wires:
            wires = _wire_list(getattr(tape, "wires", None))
        return _execute_operations(getattr(tape, "operations", []), wires)

    if hasattr(circuit, "operations"):
        wires = _wire_list(getattr(circuit, "wires", None))
        if not wires:
            for attr in ("num_wires", "n_wires", "num_qubits"):
                if hasattr(circuit, attr):
                    wires = _wire_list(getattr(circuit, attr))
                    break
        return _execute_operations(circuit.operations, wires)

    if callable(circuit):
        with qml.queuing.AnnotatedQueue() as queue:
            circuit()
        tape = qml.tape.QuantumScript.from_queue(queue)
        return _execute_operations(tape.operations, _wire_list(tape.wires))

    raise TypeError("Unsupported circuit type")
