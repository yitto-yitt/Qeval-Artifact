# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def equivalent_clifford_circuit(circuit, n):
    num_qubits = len(circuit.wires)
    target_u = qml.matrix(circuit, wire_order=range(num_qubits))
    qc_list = []
    counter = 0

    while counter < n:
        rand_cliff = qml.ops.RandomLayers.random(num_wires=num_qubits, n_layers=max(1, 2 * num_qubits), ratio_imprim=1.0, seed=np.random.randint(0, 2**31 - 1))
        rand_u = qml.matrix(rand_cliff, wire_order=range(num_qubits))

        if np.allclose(rand_u, target_u, rtol=0.4, atol=0.4):
            qc_list.append(rand_cliff)
            counter += 1

    return qc_list
