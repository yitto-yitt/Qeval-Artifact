# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np


def decompose_unitary(unitary):
    mat = cirq.unitary(unitary, default=None)
    if mat is None:
        mat = getattr(unitary, "data", unitary)
    mat = np.asarray(mat, dtype=complex)

    q0, q1 = cirq.LineQubit.range(2)
    ops = cirq.two_qubit_matrix_to_cz_operations(
        q0, q1, mat, allow_partial_czs=False, clean_operations=True
    )

    def global_phase_op(coefficient):
        return cirq.global_phase_operation(coefficient)

    def convert_czpow(op):
        gate = op.gate
        a, b = op.qubits
        exponent = float(gate.exponent)
        global_shift = float(getattr(gate, "global_shift", 0.0))
        nearest_full = 1.0 + 2.0 * round((exponent - 1.0) / 2.0)

        if abs(exponent - nearest_full) < 1e-8:
            phase = np.exp(1j * np.pi * exponent * global_shift)
            if not np.allclose(phase, 1.0, atol=1e-12):
                yield global_phase_op(phase)
            yield cirq.H(b)
            yield cirq.CNOT(a, b)
            yield cirq.H(b)
            return

        phi = np.pi * exponent
        phase = np.exp(1j * (np.pi * exponent * global_shift + phi / 4.0))
        if not np.allclose(phase, 1.0, atol=1e-12):
            yield global_phase_op(phase)
        yield cirq.rz(phi / 2.0).on(a)
        yield cirq.rz(phi / 2.0).on(b)
        yield cirq.CNOT(a, b)
        yield cirq.rz(-phi / 2.0).on(b)
        yield cirq.CNOT(a, b)

    converted_ops = []
    for op in cirq.flatten_op_tree(ops):
        if isinstance(getattr(op, "gate", None), cirq.CZPowGate):
            converted_ops.extend(convert_czpow(op))
        else:
            converted_ops.append(op)

    return cirq.Circuit(converted_ops)
