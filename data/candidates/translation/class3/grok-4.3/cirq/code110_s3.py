# EVAL_META: task_id=110, framework=cirq, class=3
import numpy as np
import cirq

def equivalent_clifford_circuit(circuit, n):
    op_or = cirq.unitary(circuit)
    num_qubits = circuit.num_qubits
    qc_list = []
    counter = 0
    qubits = cirq.LineQubit.range(num_qubits)
    while counter < n:
        rand_cliff = cirq.random_clifford(num_qubits)
        qc = cirq.Circuit(rand_cliff.on(*qubits))
        op_qc = cirq.unitary(qc)
        phase = 1.0
        for i in range(op_or.shape[0]):
            for j in range(op_or.shape[1]):
                if abs(op_or[i, j]) > 1e-4:
                    if abs(op_qc[i, j]) > 1e-4:
                        phase = op_qc[i, j] / op_or[i, j]
                        phase = phase / abs(phase)
                    break
            else:
                continue
            break
        if np.allclose(op_or, op_qc * np.conj(phase), rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
