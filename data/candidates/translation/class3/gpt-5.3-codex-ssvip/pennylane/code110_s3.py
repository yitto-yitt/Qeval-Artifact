# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def equivalent_clifford_circuit(circuit, n):
    op_or = qml.matrix(circuit)
    num_qubits = len(circuit.wires)
    qc_list = []
    counter = 0

    while counter < n:
        qc = qml.ops.RandomLayers(
            weights=np.random.uniform(0, 2 * np.pi, size=(1, num_qubits)),
            wires=range(num_qubits),
            ratio_imprim=0.0,
            seed=np.random.randint(0, 10**9),
        )
        op_qc = qml.matrix(qc)
        if np.allclose(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)

    return qc_list
