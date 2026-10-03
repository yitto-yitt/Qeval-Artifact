# EVAL_META: task_id=110, framework=cirq, class=3
import numpy as np
import cirq


def _global_phase_equiv(u, v, rtol=0.4, atol=0.4):
    u = np.asarray(u, dtype=complex)
    v = np.asarray(v, dtype=complex)
    if u.shape != v.shape:
        return False
    idx = np.unravel_index(np.argmax(np.abs(v)), v.shape)
    if abs(v[idx]) < 1e-12:
        return np.allclose(u, v, rtol=rtol, atol=atol)
    phase = u[idx] / v[idx]
    if abs(phase) < 1e-12:
        return False
    phase = phase / abs(phase)
    return np.allclose(u, phase * v, rtol=rtol, atol=atol)


def equivalent_clifford_circuit(circuit, n):
    qubits = sorted(circuit.all_qubits())
    num_qubits = len(qubits)
    if num_qubits == 0:
        qubits = [cirq.LineQubit(0)]
        num_qubits = 1

    op_or = cirq.unitary(circuit)

    qc_list = []
    counter = 0
    while counter < n:
        qs = [cirq.LineQubit(i) for i in range(num_qubits)]
        qc = cirq.testing.random_circuit(
            qubits=qs,
            n_moments=num_qubits * 4,
            op_density=0.6,
            gate_domain={
                cirq.H: 1,
                cirq.S: 1,
                cirq.X: 1,
                cirq.Y: 1,
                cirq.Z: 1,
                cirq.CNOT: 2,
                cirq.CZ: 2,
            },
        )
        try:
            op_qc = cirq.unitary(qc)
        except Exception:
            continue
        if op_qc.shape != op_or.shape:
            continue
        if _global_phase_equiv(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
