# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np
from cirq.testing import random_clifford_circuit

def equivalent_clifford_circuit(circuit: cirq.Circuit, n: int):
    qubits = sorted(list(circuit.all_qubits()))
    op_or = cirq.unitary(circuit, qubit_order=qubits)
    qc_list = []
    counter = 0
    gate_count = max(10, 5 * len(qubits))
    while counter < n:
        qc = random_clifford_circuit(qubits, gate_count=gate_count)
        op_qc = cirq.unitary(qc, qubit_order=qubits)
        
        idx = np.unravel_index(np.argmax(np.abs(op_or)), op_or.shape)
        phase = op_qc[idx] / op_or[idx]
        if np.abs(phase) > 1e-9:
            phase /= np.abs(phase)
        else:
            phase = 1.0
        
        if np.allclose(op_qc, op_or * phase, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
