# EVAL_META: task_id=110, framework=cirq, class=3
import numpy as np
import cirq
from cirq.testing import random_clifford_tableau

def equivalent_clifford_circuit(circuit, n):
    target_u = cirq.unitary(circuit)
    num_qubits = len(circuit.all_qubits())
    qc_list = []

    while len(qc_list) < n:
        tableau = random_clifford_tableau(num_qubits)
        qc = tableau.to_circuit()
        qc_u = cirq.unitary(qc)

        if qc_u.shape != target_u.shape:
            continue

        idx = int(np.argmax(np.abs(target_u)))
        denom = qc_u.flat[idx]
        if denom == 0:
            continue

        phase = target_u.flat[idx] / denom
        if np.allclose(target_u, qc_u * phase, rtol=0.4, atol=0.4):
            qc_list.append(qc)

    return qc_list
