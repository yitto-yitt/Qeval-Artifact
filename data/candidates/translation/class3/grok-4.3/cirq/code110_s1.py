# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    op_or = cirq.unitary(circuit)
    num_qubits = circuit.num_qubits
    qc_list = []
    counter = 0
    qubits = cirq.LineQubit.range(num_qubits)
    while counter < n:
        random_tableau = cirq.random_clifford(num_qubits)
        cliff_gate = cirq.Clifford(random_tableau)
        qc = cirq.Circuit(cliff_gate.on(*qubits))
        op_qc = cirq.unitary(qc)
        def normalize_phase(u):
            if abs(u[0, 0]) < 1e-10:
                for i in range(u.shape[0]):
                    for j in range(u.shape[1]):
                        if abs(u[i, j]) > 1e-10:
                            phase = np.exp(-1j * np.angle(u[i, j]))
                            return u * phase
            phase = np.exp(-1j * np.angle(u[0, 0]))
            return u * phase
        u1 = normalize_phase(op_or)
        u2 = normalize_phase(op_qc)
        if np.allclose(u1, u2, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
