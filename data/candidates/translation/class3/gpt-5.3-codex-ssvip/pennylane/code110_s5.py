# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def equivalent_clifford_circuit(circuit, n):
    op_or = qml.matrix(circuit)
    num_qubits = len(circuit.wires)
    qc_list = []
    while len(qc_list) < n:
        qc = qml.RandomLayers.compute_decomposition(
            weights=np.random.uniform(0, 2 * np.pi, size=(1, num_qubits)),
            wires=range(num_qubits),
            ratio_imprim=1.0,
            rotations=[qml.RX, qml.RY, qml.RZ],
            seed=np.random.randint(0, 10**9),
        )
        # Project to Clifford-like random circuit by replacing with random Clifford gates
        clifford_ops = []
        for w in range(num_qubits):
            g = np.random.choice(["I", "X", "Y", "Z", "H", "S"])
            if g == "X":
                clifford_ops.append(qml.PauliX(wires=w))
            elif g == "Y":
                clifford_ops.append(qml.PauliY(wires=w))
            elif g == "Z":
                clifford_ops.append(qml.PauliZ(wires=w))
            elif g == "H":
                clifford_ops.append(qml.Hadamard(wires=w))
            elif g == "S":
                clifford_ops.append(qml.S(wires=w))
        for _ in range(max(1, num_qubits // 2)):
            a, b = np.random.choice(num_qubits, size=2, replace=False)
            clifford_ops.append(qml.CNOT(wires=[a, b]))
        op_qc = qml.matrix(qml.tape.QuantumScript(ops=clifford_ops))
        if np.allclose(op_qc, op_or, rtol=0.4, atol=0.4):
            qc_list.append(qml.tape.QuantumScript(ops=clifford_ops))
    return qc_list
