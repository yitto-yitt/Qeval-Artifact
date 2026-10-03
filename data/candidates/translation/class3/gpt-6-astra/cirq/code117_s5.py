# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np


def decompose_unitary(unitary):
    matrix = np.asarray(unitary, dtype=np.complex128)
    q0, q1 = cirq.LineQubit.range(2)
    operations = cirq.two_qubit_matrix_to_cz_operations(
        q0, q1, matrix, allow_partial_czs=False, atol=1e-12
    )

    circuit = cirq.Circuit()
    for operation in operations:
        gate = operation.gate
        if isinstance(gate, cirq.CZPowGate):
            control, target = operation.qubits
            circuit.append(
                [
                    cirq.H(target),
                    cirq.CXPowGate(
                        exponent=gate.exponent,
                        global_shift=gate.global_shift,
                    )(control, target),
                    cirq.H(target),
                ]
            )
        else:
            circuit.append(operation)

    synthesized = circuit.unitary(qubit_order=[q0, q1])
    phase = np.vdot(synthesized, matrix)
    circuit.append(cirq.global_phase_operation(phase / abs(phase)))
    return circuit
