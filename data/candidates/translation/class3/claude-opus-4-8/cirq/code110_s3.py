# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np


def _equiv(u, v, rtol=0.4, atol=0.4):
    d = u.shape[0]
    inner = np.vdot(u.flatten(), v.flatten())
    phase = inner / d
    if abs(abs(phase) - 1.0) > atol:
        return False
    return np.allclose(u, phase * v, rtol=rtol, atol=atol)


def equivalent_clifford_circuit(circuit, n):
    qubits = sorted(circuit.all_qubits())
    num_qubits = len(qubits)
    op_or = cirq.unitary(circuit)

    qc_list = []
    counter = 0
    while counter < n:
        new_qubits = cirq.LineQubit.range(num_qubits)
        qc = cirq.testing.random_circuit(
            qubits=new_qubits,
            n_moments=max(1, 2 * num_qubits),
            op_density=0.8,
            gate_domain={
                cirq.H: 1,
                cirq.S: 1,
                cirq.X: 1,
                cirq.Y: 1,
                cirq.Z: 1,
                cirq.CNOT: 2,
            },
        )
        op_qc = cirq.unitary(qc)
        if op_qc.shape != op_or.shape:
            continue
        if _equiv(op_qc, op_or):
            counter += 1
            qc_list.append(qc)
    return qc_list
