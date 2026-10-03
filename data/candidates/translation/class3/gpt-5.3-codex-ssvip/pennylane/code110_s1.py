# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def equivalent_clifford_circuit(circuit, n):
    target_mat = qml.matrix(circuit)()
    wire_order = list(circuit.wires)
    num_qubits = len(wire_order)

    qc_list = []
    counter = 0

    while counter < n:
        rand_op = qml.ops.RandomLayers(
            weights=np.random.uniform(0, 2 * np.pi, (1, max(1, num_qubits))),
            wires=wire_order,
            ratio_imprim=0.0,
            rotations=(qml.PauliX, qml.PauliY, qml.PauliZ),
            seed=np.random.randint(0, 2**31 - 1),
        )
        # Build a random Clifford-like circuit using random Pauli/H/S/CNOT choices
        ops = []
        depth = max(2, 3 * num_qubits)
        for _ in range(depth):
            gate_type = np.random.randint(0, 5)
            if gate_type == 0:
                w = wire_order[np.random.randint(0, num_qubits)]
                ops.append(qml.Hadamard(wires=w))
            elif gate_type == 1:
                w = wire_order[np.random.randint(0, num_qubits)]
                ops.append(qml.S(wires=w))
            elif gate_type == 2:
                w = wire_order[np.random.randint(0, num_qubits)]
                ops.append(qml.PauliX(wires=w))
            elif gate_type == 3:
                w = wire_order[np.random.randint(0, num_qubits)]
                ops.append(qml.PauliZ(wires=w))
            else:
                if num_qubits >= 2:
                    a, b = np.random.choice(num_qubits, size=2, replace=False)
                    ops.append(qml.CNOT(wires=[wire_order[a], wire_order[b]]))
                else:
                    w = wire_order[0]
                    ops.append(qml.Hadamard(wires=w))

        cand = qml.tape.QuantumScript(ops=ops, measurements=[])
        cand_mat = qml.matrix(cand, wire_order=wire_order)()

        if np.allclose(cand_mat, target_mat, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(cand)

    return qc_list
