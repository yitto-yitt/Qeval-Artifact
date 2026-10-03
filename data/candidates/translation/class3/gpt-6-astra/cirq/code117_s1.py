# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np


def decompose_unitary(unitary):
    matrix = np.asarray(unitary, dtype=np.complex128)
    q0, q1 = cirq.LineQubit.range(2)
    operations = cirq.two_qubit_matrix_to_cz_operations(
        q0, q1, matrix, allow_partial_czs=False, clean_operations=True
    )

    circuit = cirq.Circuit()
    for operation in operations:
        if operation.gate == cirq.CZ:
            control, target = operation.qubits
            circuit.append(
                [cirq.H(target), cirq.CNOT(control, target), cirq.H(target)]
            )
        else:
            circuit.append(operation)

    for qubit in (q0, q1):
        if qubit not in circuit.all_qubits():
            circuit.append(cirq.I(qubit))

    synthesized = circuit.unitary(qubit_order=[q0, q1])
    phase = np.vdot(synthesized, matrix) / 4
    circuit.append(cirq.global_phase_operation(phase / abs(phase)))
    return circuit
