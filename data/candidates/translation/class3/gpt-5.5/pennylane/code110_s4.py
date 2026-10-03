# EVAL_META: task_id=110, framework=pennylane, class=3
import copy
import random
import pennylane as qml

def equivalent_clifford_circuit(circuit, n):
    def _to_script(obj):
        if hasattr(obj, "operations") and hasattr(obj, "wires"):
            return obj

        if isinstance(obj, (list, tuple)):
            return qml.tape.QuantumScript(ops=list(obj), measurements=[])

        for attr in ("qtape", "tape", "_tape"):
            try:
                tape = getattr(obj, attr)
            except Exception:
                tape = None
            if tape is not None and hasattr(tape, "operations"):
                return tape

        if hasattr(obj, "func"):
            try:
                return qml.tape.make_qscript(obj.func)()
            except Exception:
                pass

        if hasattr(obj, "construct"):
            try:
                obj.construct([], {})
                for attr in ("qtape", "tape", "_tape"):
                    tape = getattr(obj, attr, None)
                    if tape is not None and hasattr(tape, "operations"):
                        return tape
            except Exception:
                pass

        if callable(obj):
            try:
                return qml.tape.make_qscript(obj)()
            except Exception:
                pass

        raise TypeError("Unsupported PennyLane circuit object.")

    def _copy_op(op):
        try:
            return copy.copy(op)
        except Exception:
            return op

    def _identity_block(wires):
        if len(wires) > 1 and random.random() < 0.5:
            a, b = random.sample(wires, 2)
            gate = random.randrange(3)
            if gate == 0:
                return [qml.CNOT(wires=[a, b]), qml.CNOT(wires=[a, b])]
            if gate == 1:
                return [qml.CZ(wires=[a, b]), qml.CZ(wires=[a, b])]
            return [qml.SWAP(wires=[a, b]), qml.SWAP(wires=[a, b])]

        w = random.choice(wires)
        gate = random.randrange(5)
        if gate == 0:
            return [qml.Hadamard(wires=w), qml.Hadamard(wires=w)]
        if gate == 1:
            return [qml.PauliX(wires=w), qml.PauliX(wires=w)]
        if gate == 2:
            return [qml.PauliY(wires=w), qml.PauliY(wires=w)]
        if gate == 3:
            return [qml.PauliZ(wires=w), qml.PauliZ(wires=w)]
        return [qml.S(wires=w), qml.S(wires=w), qml.S(wires=w), qml.S(wires=w)]

    script = _to_script(circuit)
    base_ops = list(getattr(script, "operations", []))

    wires = []
    try:
        if hasattr(circuit, "device") and getattr(circuit.device, "wires", None) is not None:
            device_wires = list(circuit.device.wires)
            if len(device_wires) > 0:
                wires = device_wires
    except Exception:
        wires = []

    if not wires:
        try:
            wires = list(script.wires)
        except Exception:
            wires = []

    if not wires:
        seen = set()
        for op in base_ops:
            for w in op.wires:
                if w not in seen:
                    seen.add(w)
                    wires.append(w)

    circuits = []
    counter = 0
    while counter < n:
        ops = []

        for w in wires:
            ops.extend([qml.Hadamard(wires=w), qml.Hadamard(wires=w)])

        ops.extend(_copy_op(op) for op in base_ops)

        if wires:
            for _ in range(random.randint(1, max(1, 2 * len(wires)))):
                ops.extend(_identity_block(wires))

        circuits.append(qml.tape.QuantumScript(ops=ops, measurements=[]))
        counter += 1

    return circuits
