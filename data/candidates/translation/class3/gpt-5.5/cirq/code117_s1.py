# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np


def decompose_unitary(unitary):
    if isinstance(unitary, np.ndarray):
        u = unitary
    elif hasattr(unitary, "data"):
        u = unitary.data
    else:
        u = unitary
    u = np.asarray(u, dtype=complex)

    q0, q1 = cirq.LineQubit.range(2)
    qubits = (q0, q1)

    cz_ops = cirq.two_qubit_matrix_to_cz_operations(
        q0, q1, u, allow_partial_czs=False, clean_operations=True, atol=1e-8
    )

    ops = []
    for op in cz_ops:
        gate = op.gate
        if isinstance(gate, cirq.CZPowGate):
            a, b = op.qubits
            exponent = float(gate.exponent)
            if np.isclose(np.mod(exponent - 1.0, 2.0), 0.0, atol=1e-8):
                ops.extend([cirq.H(b), cirq.CNOT(a, b), cirq.H(b)])
            elif np.isclose(np.mod(exponent, 2.0), 0.0, atol=1e-8):
                continue
            else:
                phi = np.pi * exponent
                ops.extend(
                    [
                        cirq.rz(phi / 2).on(a),
                        cirq.rz(phi / 2).on(b),
                        cirq.CNOT(a, b),
                        cirq.rz(-phi / 2).on(b),
                        cirq.CNOT(a, b),
                    ]
                )
        else:
            ops.append(op)

    circuit = cirq.Circuit(ops)

    current = circuit.unitary(qubit_order=qubits)
    idx = int(np.argmax(np.abs(u)))
    if abs(current.flat[idx]) > 1e-12:
        phase = u.flat[idx] / current.flat[idx]
        if abs(phase) > 0:
            phase = phase / abs(phase)
            if not np.isclose(phase, 1.0, atol=1e-8):
                circuit = cirq.Circuit(
                    cirq.global_phase_operation(coefficient=phase),
                    *circuit.all_operations(),
                )

    return circuit
