# EVAL_META: task_id=110, framework=cirq, class=3

import numpy as np
import cirq

def _operator_equiv(mat1, mat2, rtol=0.4, atol=0.4):
    norm1 = np.linalg.norm(mat1)
    norm2 = np.linalg.norm(mat2)
    phase = np.vdot(mat1, mat2) / (norm1 * norm2)
    if abs(phase) < 1e-10:
        return False
    phase = phase / abs(phase)
    return np.allclose(mat1, phase * mat2, rtol=rtol, atol=atol)

def equivalent_clifford_circuit(circuit, n):
    op_or = cirq.unitary(circuit)
    num_qubits = len(circuit.all_qubits())
    qc_list = []
    counter = 0
    while counter < n:
        qc = cirq.CliffordTableau.random(num_qubits).to_circuit()
        op_qc = cirq.unitary(qc)
        if _operator_equiv(op_qc, op_or):
            counter += 1
            qc_list.append(qc)
    return qc_list
