# EVAL_META: task_id=110, framework=pennylane, class=3
import copy
import numpy as np
import pennylane as qml

def equivalent_clifford_circuit(circuit, n):
    def _copy_obj(obj):
        try:
            return obj.copy()
        except Exception:
            return copy.deepcopy(obj)

    def _to_script(obj):
        if isinstance(obj, qml.tape.QuantumScript):
            return obj

        if hasattr(obj, "construct") and hasattr(obj, "device"):
            try:
                obj.construct((), {})
                tape = getattr(obj, "qtape", None) or getattr(obj, "_tape", None)
                if tape is not None:
                    return tape
            except Exception:
                pass

        if callable(obj):
            try:
                with qml.queuing.AnnotatedQueue() as q:
                    obj()
                return qml.tape.QuantumScript.from_queue(q)
            except Exception:
                pass

        if hasattr(obj, "operations"):
            ops = list(getattr(obj, "operations", []))
            measurements = list(getattr(obj, "measurements", []))
            shots = getattr(obj, "shots", None)
            return qml.tape.QuantumScript(ops, measurements, shots=shots)

        if isinstance(obj, (list, tuple)):
            return qml.tape.QuantumScript(list(obj), [])

        return qml.tape.QuantumScript([], [])

    script = _to_script(circuit)

    wires = list(getattr(script, "wires", []))
    if not wires and hasattr(circuit, "device") and hasattr(circuit.device, "wires"):
        wires = list(circuit.device.wires)
    if not wires and hasattr(circuit, "num_wires"):
        try:
            wires = list(range(int(circuit.num_wires)))
        except Exception:
            pass
    if not wires and hasattr(circuit, "num_qubits"):
        try:
            wires = list(range(int(circuit.num_qubits)))
        except Exception:
            pass

    rng = np.random.default_rng()
    shots = getattr(script, "shots", None)

    def _gate(name, gate_wires):
        if name == "H":
            return qml.Hadamard(wires=gate_wires)
        if name == "X":
            return qml.PauliX(wires=gate_wires)
        if name == "Y":
            return qml.PauliY(wires=gate_wires)
        if name == "Z":
            return qml.PauliZ(wires=gate_wires)
        if name == "CNOT":
            return qml.CNOT(wires=gate_wires)
        if name == "CZ":
            return qml.CZ(wires=gate_wires)
        return qml.SWAP(wires=gate_wires)

    def _random_identity_block():
        if not wires:
            return []
        with qml.queuing.QueuingManager.stop_recording():
            if len(wires) >= 2 and rng.random() < 0.5:
                names = ("CNOT", "CZ", "SWAP")
                name = names[int(rng.integers(len(names)))]
                inds = rng.choice(len(wires), size=2, replace=False)
                gate_wires = [wires[int(inds[0])], wires[int(inds[1])]]
            else:
                names = ("H", "X", "Y", "Z")
                name = names[int(rng.integers(len(names)))]
                gate_wires = wires[int(rng.integers(len(wires)))]
            return [_gate(name, gate_wires), _gate(name, gate_wires)]

    circuits = []
    for _ in range(int(n)):
        with qml.queuing.QueuingManager.stop_recording():
            ops = [_copy_obj(op) for op in getattr(script, "operations", [])]
            for w in wires:
                ops.append(qml.Identity(wires=w))
            for __ in range(int(rng.integers(1, max(2, len(wires) + 2)))):
                ops.extend(_random_identity_block())
            measurements = [_copy_obj(m) for m in getattr(script, "measurements", [])]
            circuits.append(qml.tape.QuantumScript(ops, measurements, shots=shots))

    return circuits
