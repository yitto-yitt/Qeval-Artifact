# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml
from pennylane.tape import QuantumTape


def equivalent_clifford_circuit(circuit, n):
    rng = np.random.default_rng()
    wires, base_ops = _get_wires_and_ops(circuit)
    wire_list = list(wires)

    qc_list = []
    for _ in range(n):
        half_length = int(rng.integers(3, 8))
        specs = _random_specs(wire_list, half_length, rng)
        identity_ops = _specs_to_ops(specs) + _inverse_ops_from_specs(list(reversed(specs)))
        new_ops = list(base_ops) + identity_ops
        qc_list.append(QuantumTape(new_ops, []))

    return qc_list


def _get_wires_and_ops(circuit):
    if isinstance(circuit, QuantumTape):
        return circuit.wires, circuit.operations

    try:
        tape = circuit.tape
        if tape is None:
            raise ValueError("No tape")
    except Exception:
        _ = qml.matrix(circuit)()
        tape = circuit.tape

    return tape.wires, tape.operations


def _random_specs(wire_list, length, rng):
    n = len(wire_list)
    specs = []

    for _ in range(length):
        if n == 0:
            break

        if n == 1:
            gate = rng.choice(["H", "S"])
        else:
            gate = rng.choice(["H", "S", "CNOT", "CZ", "SWAP"])

        if gate in ("H", "S"):
            idx = int(rng.integers(n))
            specs.append((gate, wire_list[idx]))
        else:
            if n < 2:
                continue
            i, j = rng.choice(n, size=2, replace=False)
            specs.append((gate, wire_list[i], wire_list[j]))

    return specs


def _specs_to_ops(specs):
    ops = []
    for spec in specs:
        gate = spec[0]

        if gate == "H":
            ops.append(qml.Hadamard(wires=spec[1]))
        elif gate == "S":
            ops.append(qml.S(wires=spec[1]))
        elif gate == "CNOT":
            ops.append(qml.CNOT(wires=[spec[1], spec[2]]))
        elif gate == "CZ":
            ops.append(qml.CZ(wires=[spec[1], spec[2]]))
        elif gate == "SWAP":
            ops.append(qml.SWAP(wires=[spec[1], spec[2]]))

    return ops


def _inverse_ops_from_specs(specs):
    ops = []
    for spec in specs:
        gate = spec[0]

        if gate == "S":
            ops.append(qml.S(wires=spec[1]))
            ops.append(qml.S(wires=spec[1]))
            ops.append(qml.S(wires=spec[1]))
        else:
            ops.extend(_specs_to_ops([spec]))

    return ops
