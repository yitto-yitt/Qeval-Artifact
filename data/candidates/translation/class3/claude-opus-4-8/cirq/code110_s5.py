# EVAL_META: task_id=110, framework=cirq, class=3
import numpy as np
import cirq


def _unitary_equiv(u1, u2, rtol=0.4, atol=0.4):
    d = u1.shape[0]
    prod = u1.conj().T @ u2
    phase = np.trace(prod) / d
    if abs(phase) < 1e-12:
        return False
    phase = phase / abs(phase)
    return np.allclose(u1, phase * u2, rtol=rtol, atol=atol)


def equivalent_clifford_circuit(circuit, n):
    qubits = sorted(circuit.all_qubits())
    if not qubits:
        qubits = [cirq.LineQubit(0)]
    num_qubits = len(qubits)
    target = cirq.unitary(circuit)

    qc_list = []
    counter = 0
    while counter < n:
        qc = _random_clifford_circuit(num_qubits)
        u = qc.unitary(qubit_order=qubits) if False else cirq.unitary(qc)
        if _unitary_equiv(u, target):
            counter += 1
            qc_list.append(qc)
    return qc_list


def _random_clifford_circuit(num_qubits):
    qubits = [cirq.LineQubit(i) for i in range(num_qubits)]
    circuit = cirq.Circuit()
    single_gates = [cirq.H, cirq.S, cirq.X, cirq.Y, cirq.Z, cirq.I]
    depth = 4 * num_qubits + 4
    for _ in range(depth):
        for q in qubits:
            g = single_gates[np.random.randint(len(single_gates))]
            circuit.append(g(q))
        if num_qubits > 1:
            for _ in range(num_qubits):
                a = np.random.randint(num_qubits)
                b = np.random.randint(num_qubits)
                if a != b:
                    circuit.append(cirq.CNOT(qubits[a], qubits[b]))
    return circuit
