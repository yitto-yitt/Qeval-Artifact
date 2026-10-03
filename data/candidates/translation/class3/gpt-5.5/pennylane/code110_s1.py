# EVAL_META: task_id=110, framework=pennylane, class=3
import copy
import random
import pennylane as qml


def equivalent_clifford_circuit(circuit, n):
    def _get_base(obj):
        if hasattr(obj, "operations"):
            return obj
        if hasattr(obj, "qtape") and hasattr(obj.qtape, "operations"):
            return obj.qtape
        if hasattr(obj, "_tape") and hasattr(obj._tape, "operations"):
            return obj._tape
        return obj

    def _wire_list(obj):
        if hasattr(obj, "wires"):
            try:
                return list(obj.wires)
            except TypeError:
                pass
        if hasattr(obj, "num_wires"):
            return list(range(obj.num_wires))
        if hasattr(obj, "num_qubits"):
            return list(range(obj.num_qubits))
        return []

    def _identity_ops(wires):
        if not wires:
            return []
        ops = []
        reps = random.randint(1, 4)
        for _ in range(reps):
            w = random.choice(wires)
            gate = random.choice(("H", "X", "Y", "Z", "S"))
            if gate == "H":
                ops.extend([qml.Hadamard(wires=w), qml.Hadamard(wires=w)])
            elif gate == "X":
                ops.extend([qml.PauliX(wires=w), qml.PauliX(wires=w)])
            elif gate == "Y":
                ops.extend([qml.PauliY(wires=w), qml.PauliY(wires=w)])
            elif gate == "Z":
                ops.extend([qml.PauliZ(wires=w), qml.PauliZ(wires=w)])
            else:
                ops.extend([qml.S(wires=w), qml.S(wires=w), qml.S(wires=w), qml.S(wires=w)])
        return ops

    base = _get_base(circuit)
    wires = _wire_list(base)

    if hasattr(base, "operations"):
        circuits = []
        for _ in range(n):
            prefix = _identity_ops(wires)
            ops = prefix + [copy.copy(op) for op in base.operations]
            measurements = [copy.copy(m) for m in getattr(base, "measurements", [])]
            shots = getattr(base, "shots", None)
            circuits.append(qml.tape.QuantumScript(ops, measurements, shots=shots))
        return circuits

    if callable(circuit):
        circuits = []
        for _ in range(n):
            specs = []
            for op in _identity_ops(wires):
                specs.append((op.name, tuple(op.wires)))

            def wrapped(*args, _circuit=circuit, _specs=specs, **kwargs):
                for name, op_wires in _specs:
                    w = op_wires[0] if len(op_wires) == 1 else list(op_wires)
                    if name == "Hadamard":
                        qml.Hadamard(wires=w)
                    elif name == "PauliX":
                        qml.PauliX(wires=w)
                    elif name == "PauliY":
                        qml.PauliY(wires=w)
                    elif name == "PauliZ":
                        qml.PauliZ(wires=w)
                    elif name == "S":
                        qml.S(wires=w)
                return _circuit(*args, **kwargs)

            circuits.append(wrapped)
        return circuits

    return [copy.copy(circuit) for _ in range(n)]
