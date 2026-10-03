# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    matrix = np.asarray(unitary, dtype=complex)

    ops = cirq.two_qubit_matrix_to_cz_operations(
        q0, q1, matrix, allow_partial_czs=False
    )

    converted_ops = []
    for op in ops:
        gate = getattr(op, "gate", None)
        if isinstance(gate, cirq.CZPowGate):
            a, b = op.qubits
            exponent = float(gate.exponent)
            global_shift = float(getattr(gate, "global_shift", 0.0))
            global_coeff = np.exp(1j * np.pi * exponent * global_shift)

            if not np.isclose(global_coeff, 1.0):
                converted_ops.append(cirq.global_phase_operation(global_coeff))

            if np.isclose(np.mod(exponent, 2.0), 1.0):
                converted_ops.extend([cirq.H(b), cirq.CNOT(a, b), cirq.H(b)])
            elif not np.isclose(np.mod(exponent, 2.0), 0.0):
                theta = np.pi * exponent
                converted_ops.append(cirq.global_phase_operation(np.exp(1j * theta / 4.0)))
                converted_ops.extend([
                    cirq.rz(theta / 2.0).on(a),
                    cirq.rz(theta / 2.0).on(b),
                    cirq.CNOT(a, b),
                    cirq.rz(-theta / 2.0).on(b),
                    cirq.CNOT(a, b),
                ])
        else:
            converted_ops.append(op)

    return cirq.Circuit(converted_ops)
