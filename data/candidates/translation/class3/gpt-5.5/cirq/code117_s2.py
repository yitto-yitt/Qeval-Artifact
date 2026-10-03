# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    mat = np.asarray(getattr(unitary, "data", unitary), dtype=complex)
    q0, q1 = cirq.LineQubit.range(2)

    ops = cirq.two_qubit_matrix_to_cz_operations(
        q0, q1, mat, allow_partial_czs=False, clean_operations=True
    )

    converted_ops = []
    accumulated_phase = 1.0 + 0.0j

    for op in cirq.flatten_op_tree(ops):
        gate = getattr(op, "gate", None)
        if isinstance(gate, cirq.CZPowGate):
            a, b = op.qubits
            exponent = float(gate.exponent)
            global_shift = float(getattr(gate, "global_shift", 0.0))
            if np.isclose(np.mod(exponent, 2.0), 1.0, atol=1e-8):
                accumulated_phase *= np.exp(1j * np.pi * global_shift * exponent)
                converted_ops.extend([cirq.H(b), cirq.CNOT(a, b), cirq.H(b)])
            else:
                theta = np.pi * exponent
                accumulated_phase *= np.exp(1j * np.pi * global_shift * exponent + 1j * theta / 4.0)
                converted_ops.extend([
                    cirq.rz(theta / 2.0)(a),
                    cirq.rz(theta / 2.0)(b),
                    cirq.CNOT(a, b),
                    cirq.rz(-theta / 2.0)(b),
                    cirq.CNOT(a, b),
                ])
        else:
            converted_ops.append(op)

    if not np.isclose(accumulated_phase, 1.0 + 0.0j, atol=1e-10):
        converted_ops.append(cirq.global_phase_operation(coefficient=complex(accumulated_phase)))

    circuit = cirq.Circuit(converted_ops)

    try:
        current = circuit.unitary(qubit_order=[q0, q1])
        idx = np.unravel_index(np.argmax(np.abs(current)), current.shape)
        if abs(current[idx]) > 1e-12:
            phase = mat[idx] / current[idx]
            if abs(phase) > 0:
                phase = phase / abs(phase)
            if np.allclose(phase * current, mat, atol=1e-7) and not np.isclose(phase, 1.0 + 0.0j, atol=1e-10):
                circuit.append(cirq.global_phase_operation(coefficient=complex(phase)))
    except Exception:
        pass

    return circuit
