# EVAL_META: task_id=110, framework=cirq, class=3
import numpy as np
import cirq


def equivalent_clifford_circuit(circuit, n):
    num_qubits = len(circuit.all_qubits())
    qubits = cirq.LineQubit.range(num_qubits)
    target_u = cirq.unitary(circuit)
    qc_list = []
    while len(qc_list) < n:
        rc = cirq.testing.random_clifford_circuit(qubits)
        u = cirq.unitary(rc)
        if np.allclose(u, target_u, rtol=0.4, atol=0.4):
            qc_list.append(rc)
    return qc_list
