# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np


def decompose_unitary(unitary):
    matrix = np.asarray(unitary, dtype=np.complex128)
    qubits = cirq.LineQubit.range(2)
    operations = cirq.two_qubit_matrix_to_cz_operations(
        qubits[0],
        qubits[1],
        matrix,
        allow_partial_czs=False,
    )

    circuit = cirq.Circuit()
    for operation in operations:
        if isinstance(operation.gate, cirq.CZPowGate):
            control, target = operation.qubits
            circuit.append(
                [
                    cirq.H(target),
                    cirq.CNOT(control, target),
                    cirq.H(target),
                ]
            )
        else:
            circuit.append(operation)

    for qubit in qubits:
        if qubit not in circuit.all_qubits():
            circuit.append(cirq.I(qubit))

    synthesized = circuit.unitary(qubit_order=qubits)
    phase = np.vdot(synthesized, matrix)
    if abs(phase) > 0:
        circuit.append(cirq.global_phase_operation(phase / abs(phase)))

    return circuit
