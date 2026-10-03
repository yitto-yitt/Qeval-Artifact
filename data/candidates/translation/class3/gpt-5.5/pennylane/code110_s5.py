# EVAL_META: task_id=110, framework=pennylane, class=3
import copy
import numpy as np
import pennylane as qml

def equivalent_clifford_circuit(circuit, n):
    ops = getattr(circuit, "operations", None)
    if ops is None:
        ops = getattr(circuit, "ops", None)
    measurements = getattr(circuit, "measurements", [])

    if ops is None:
        return [copy.deepcopy(circuit) for _ in range(n)]

    ops = list(ops)
    measurements = list(measurements)

    wires = []
    circuit_wires = getattr(circuit, "wires", None)
    if circuit_wires is not None:
        try:
            wires = list(circuit_wires)
        except TypeError:
            wires = [circuit_wires]

    if not wires:
        for obj in ops + measurements:
            obj_wires = getattr(obj, "wires", [])
            for w in obj_wires:
                if w not in wires:
                    wires.append(w)

    rng = np.random.default_rng()
    circuits = []

    def add_random_identity(target_ops):
        if not wires:
            return

        reps = int(rng.integers(1, max(2, len(wires) + 3)))
        one_qubit_gates = (qml.Hadamard, qml.PauliX, qml.PauliY, qml.PauliZ)

        for _ in range(reps):
            if len(wires) >= 2 and rng.random() < 0.4:
                idx = rng.choice(len(wires), size=2, replace=False)
                pair_wires = [wires[int(idx[0])], wires[int(idx[1])]]
                gate_choice = int(rng.integers(3))
                if gate_choice == 0:
                    target_ops.append(qml.CNOT(wires=pair_wires))
                    target_ops.append(qml.CNOT(wires=pair_wires))
                elif gate_choice == 1:
                    target_ops.append(qml.CZ(wires=pair_wires))
                    target_ops.append(qml.CZ(wires=pair_wires))
                else:
                    target_ops.append(qml.SWAP(wires=pair_wires))
                    target_ops.append(qml.SWAP(wires=pair_wires))
            else:
                w = wires[int(rng.integers(len(wires)))]
                gate_choice = int(rng.integers(5))
                if gate_choice < 4:
                    gate = one_qubit_gates[gate_choice]
                    target_ops.append(gate(wires=w))
                    target_ops.append(gate(wires=w))
                else:
                    target_ops.append(qml.S(wires=w))
                    target_ops.append(qml.S(wires=w))
                    target_ops.append(qml.S(wires=w))
                    target_ops.append(qml.S(wires=w))

    for _ in range(n):
        new_ops = [copy.copy(op) for op in ops]
        add_random_identity(new_ops)
        new_measurements = [copy.copy(m) for m in measurements]

        try:
            new_circuit = circuit.copy(operations=new_ops, measurements=new_measurements)
        except Exception:
            shots = getattr(circuit, "shots", None)
            try:
                new_circuit = qml.tape.QuantumScript(new_ops, new_measurements, shots=shots)
            except TypeError:
                new_circuit = qml.tape.QuantumScript(new_ops, new_measurements)

        circuits.append(new_circuit)

    return circuits
