# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    try:
        mat = np.asarray(unitary, dtype=complex)
    except (TypeError, ValueError):
        mat = None

    if mat is None or mat.shape != (4, 4):
        if hasattr(unitary, "data"):
            mat = np.asarray(unitary.data, dtype=complex)
        else:
            mat = np.asarray(cirq.unitary(unitary), dtype=complex)

    q0, q1 = cirq.LineQubit.range(2)
    ops = cirq.two_qubit_matrix_to_cz_operations(
        q0, q1, mat, allow_partial_czs=False, atol=1e-10
    )

    converted_ops = []
    for op in ops:
        gate = getattr(op, "gate", None)
        if isinstance(gate, cirq.CZPowGate) and len(op.qubits) == 2:
            a, b = op.qubits
            exponent = float(gate.exponent)
            global_shift = float(getattr(gate, "global_shift", 0.0))
            mod_exp = np.mod(exponent, 2.0)

            if np.isclose(mod_exp, 1.0, atol=1e-10):
                phase = np.exp(1j * np.pi * global_shift * exponent)
                if not np.isclose(phase, 1.0, atol=1e-10):
                    converted_ops.append(cirq.global_phase_operation(phase))
                converted_ops.extend([cirq.H(b), cirq.CNOT(a, b), cirq.H(b)])
            elif np.isclose(mod_exp, 0.0, atol=1e-10) or np.isclose(mod_exp, 2.0, atol=1e-10):
                phase = np.exp(1j * np.pi * global_shift * exponent)
                if not np.isclose(phase, 1.0, atol=1e-10):
                    converted_ops.append(cirq.global_phase_operation(phase))
            else:
                theta = np.pi * exponent
                phase = np.exp(1j * np.pi * global_shift * exponent) * np.exp(1j * theta / 4)
                if not np.isclose(phase, 1.0, atol=1e-10):
                    converted_ops.append(cirq.global_phase_operation(phase))
                converted_ops.extend([
                    cirq.rz(theta / 2).on(a),
                    cirq.rz(theta / 2).on(b),
                    cirq.CNOT(a, b),
                    cirq.rz(-theta / 2).on(b),
                    cirq.CNOT(a, b),
                ])
        else:
            converted_ops.append(op)

    circuit = cirq.Circuit(converted_ops)

    try:
        actual = circuit.unitary(qubit_order=[q0, q1])
        idx = np.unravel_index(np.argmax(np.abs(actual)), actual.shape)
        if abs(actual[idx]) > 1e-12:
            phase = mat[idx] / actual[idx]
            if abs(phase) > 1e-12:
                phase = phase / abs(phase)
                if not np.isclose(phase, 1.0, atol=1e-10):
                    circuit = cirq.Circuit([cirq.global_phase_operation(phase), *circuit.all_operations()])
    except Exception:
        pass

    return circuit
