# EVAL_META: task_id=10, framework=cirq, class=3
import cirq
import numpy as np


def create_operator():
    matrix = np.array(
        [[0, 0, 0, 1],
         [0, 0, 1, 0],
         [0, 1, 0, 0],
         [1, 0, 0, 0]],
        dtype=complex,
    )
    q0, q1 = cirq.LineQubit.range(2)
    operations = cirq.two_qubit_matrix_to_cz_operations(
        q0, q1, matrix, allow_partial_czs=False
    )

    circuit = cirq.Circuit()
    for operation in operations:
        if isinstance(operation.gate, cirq.CZPowGate):
            control, target = operation.qubits
            circuit.append(
                [cirq.H(target), cirq.CNOT(control, target), cirq.H(target)]
            )
        elif isinstance(operation.gate, cirq.GlobalPhaseGate):
            circuit.append(
                cirq.MatrixGate(
                    operation.gate.coefficient * np.eye(2)
                ).on(q0)
            )
        else:
            circuit.append(operation)

    actual = circuit.unitary(qubit_order=[q0, q1])
    phase = np.trace(actual.conj().T @ matrix) / 4
    phase /= abs(phase)
    if not np.isclose(phase, 1, atol=1e-12, rtol=0):
        circuit.append(cirq.MatrixGate(phase * np.eye(2)).on(q0))

    return cirq.merge_single_qubit_gates_to_phased_x_and_z(circuit)
