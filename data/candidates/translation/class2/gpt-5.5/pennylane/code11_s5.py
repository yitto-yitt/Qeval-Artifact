# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml
import numpy as np


def get_statevector(circuit):
    def _as_wire_list(wires):
        if wires is None:
            return []
        try:
            return list(wires)
        except TypeError:
            return [wires]

    def _infer_wires(obj=None, ops=None):
        dev = getattr(obj, "device", None)
        if dev is not None:
            dev_wires = _as_wire_list(getattr(dev, "wires", None))
            if dev_wires:
                return dev_wires

        wires = _as_wire_list(getattr(obj, "wires", None))
        if wires:
            return wires

        num_wires = getattr(obj, "num_wires", None)
        if num_wires is not None:
            try:
                return list(range(int(num_wires)))
            except TypeError:
                pass

        if ops:
            all_wires = qml.wires.Wires.all_wires([op.wires for op in ops])
            return list(all_wires)

        return []

    def _simulate_operations(ops, wires):
        ops = list(ops)
        wires = list(wires)

        if not wires:
            wires = _infer_wires(ops=ops)

        if not wires:
            return np.array([1.0 + 0.0j], dtype=complex)

        dev = qml.device("default.qubit", wires=wires)

        @qml.qnode(dev)
        def state_circuit():
            for op in ops:
                qml.apply(op)
            return qml.state()

        return state_circuit()

    if isinstance(circuit, qml.tape.QuantumScript):
        return _simulate_operations(circuit.operations, _infer_wires(circuit, circuit.operations))

    if isinstance(circuit, qml.QNode):
        tape = None
        try:
            tape = circuit.construct((), {})
        except TypeError:
            try:
                tape = circuit.construct([], {})
            except TypeError:
                tape = None

        if tape is None:
            tape = getattr(circuit, "_tape", None) or getattr(circuit, "qtape", None)

        if tape is not None:
            return _simulate_operations(tape.operations, _infer_wires(circuit, tape.operations))

        return circuit()

    if hasattr(circuit, "operations"):
        return _simulate_operations(circuit.operations, _infer_wires(circuit, circuit.operations))

    if callable(circuit):
        with qml.queuing.AnnotatedQueue() as queue:
            circuit()
        tape = qml.tape.QuantumScript.from_queue(queue)
        return _simulate_operations(tape.operations, _infer_wires(tape, tape.operations))

    if isinstance(circuit, (list, tuple)):
        return _simulate_operations(circuit, _infer_wires(ops=circuit))

    raise TypeError("Unsupported circuit type")
