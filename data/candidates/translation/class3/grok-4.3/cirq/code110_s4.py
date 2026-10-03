# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    op_or = cirq.unitary(circuit)
    num_qubits = circuit.n_qubits
    qc_list = []
    counter = 0
    while counter < n:
        tableau = cirq.CliffordTableau.random(num_qubits)
        cliff = cirq.Clifford(tableau)
        qc = cliff.to_circuit()
        op_qc = cirq.unitary(qc)
        u1_flat = op_or.ravel()
        u2_flat = op_qc.ravel()
        idx = np.argmax(np.abs(u2_flat))
        if np.abs(u2_flat[idx]) < 1e-10:
            continue
        phase = u1_flat[idx] / u2_flat[idx]
        if np.allclose(op_or, phase * op_qc, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
