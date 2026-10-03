# EVAL_META: task_id=110, framework=pennylane, class=3
import copy
import random
import pennylane as qml


def equivalent_clifford_circuit(circuit, n):
    def _wires(c):
        if hasattr(c, "num_qubits"):
            return list(range(c.num_qubits))
        if hasattr(c, "num_wires"):
            return list(range(c.num_wires))
        if hasattr(c, "wires"):
            return list(c.wires)
        return []

    def _ops(c):
        if hasattr(c, "operations"):
            return [copy.copy(op) for op in c.operations]
        if hasattr(c, "ops"):
            return [copy.copy(op) for op in c.ops]
        return []

    def _measurements(c):
        if hasattr(c, "measurements"):
            return [copy.copy(m) for m in c.measurements]
        return []

    wires = _wires(circuit)
    base_ops = _ops(circuit)
    measurements = _measurements(circuit)
    shots = getattr(circuit, "shots", None)

    circuits = []
    for _ in range(n):
        ops = [copy.copy(op) for op in base_ops]

        if wires:
            for _ in range(random.randint(1, 5)):
                if len(wires) >= 2 and random.random() < 0.5:
                    control, target = random.sample(wires, 2)
                    gate = random.choice(("CNOT", "CZ", "SWAP"))
                    if gate == "CNOT":
                        ops.append(qml.CNOT(wires=[control, target]))
                        ops.append(qml.CNOT(wires=[control, target]))
                    elif gate == "CZ":
                        ops.append(qml.CZ(wires=[control, target]))
                        ops.append(qml.CZ(wires=[control, target]))
                    else:
                        ops.append(qml.SWAP(wires=[control, target]))
                        ops.append(qml.SWAP(wires=[control, target]))
                else:
                    wire = random.choice(wires)
                    gate = random.choice(("H", "X", "Y", "Z", "S"))
                    if gate == "H":
                        ops.append(qml.Hadamard(wires=wire))
                        ops.append(qml.Hadamard(wires=wire))
                    elif gate == "X":
                        ops.append(qml.PauliX(wires=wire))
                        ops.append(qml.PauliX(wires=wire))
                    elif gate == "Y":
                        ops.append(qml.PauliY(wires=wire))
                        ops.append(qml.PauliY(wires=wire))
                    elif gate == "Z":
                        ops.append(qml.PauliZ(wires=wire))
                        ops.append(qml.PauliZ(wires=wire))
                    else:
                        ops.append(qml.S(wires=wire))
                        ops.append(qml.adjoint(qml.S(wires=wire)))

        circuits.append(qml.tape.QuantumScript(ops, [copy.copy(m) for m in measurements], shots=shots))

    return circuits
