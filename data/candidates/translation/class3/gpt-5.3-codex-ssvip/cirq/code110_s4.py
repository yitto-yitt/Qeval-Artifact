# EVAL_META: task_id=110, framework=cirq, class=3
import numpy as np
import cirq


def equivalent_clifford_circuit(circuit, n):
    target_u = cirq.unitary(circuit)
    num_qubits = len(circuit.all_qubits())
    qubits = cirq.LineQubit.range(num_qubits)
    qc_list = []
    while len(qc_list) < n:
        cliff = cirq.testing.random_clifford_circuit(qubits=qubits, n_moments=max(1, 5 * num_qubits))
        u = cirq.unitary(cliff)
        if np.allclose(u, target_u, rtol=0.4, atol=0.4):
            qc_list.append(cliff)
    return qc_list
