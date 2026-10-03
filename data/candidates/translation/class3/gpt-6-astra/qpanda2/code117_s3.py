# EVAL_META: task_id=117, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def decompose_unitary(unitary):
    matrix = np.asarray(unitary, dtype=np.complex128)
    if matrix.shape != (4, 4):
        raise ValueError("unitary must be a 4x4 matrix.")
    if not np.allclose(matrix.conj().T @ matrix, np.eye(4), atol=1e-10):
        raise ValueError("The input matrix must be unitary.")

    circuit = None
    for positive_sequence in (False, True):
        candidate = pq.matrix_decompose(
            qubits, matrix, positive_sequence
        )
        actual = np.asarray(
            pq.get_matrix(candidate), dtype=np.complex128
        ).reshape(4, 4)
        overlap = np.vdot(matrix, actual) / 4.0
        if abs(overlap) > 0 and np.allclose(
            actual, (overlap / abs(overlap)) * matrix, atol=1e-8
        ):
            circuit = candidate
            break

    if circuit is None:
        raise RuntimeError("The framework could not reproduce the input unitary.")

    try:
        result = pq.transform_to_base_qgate(
            circuit, machine, ["U3"], ["CNOT"]
        )
        if result is not None:
            circuit = result
    except TypeError:
        program = pq.QProg()
        program << circuit
        result = pq.transform_to_base_qgate(
            program, machine, ["U3"], ["CNOT"]
        )
        circuit = pq.cast_qprog_qcircuit(
            program if result is None else result
        )

    if isinstance(circuit, pq.QProg):
        circuit = pq.cast_qprog_qcircuit(circuit)

    actual = np.asarray(
        pq.get_matrix(circuit), dtype=np.complex128
    ).reshape(4, 4)
    overlap = np.vdot(matrix, actual) / 4.0
    if abs(overlap) == 0 or not np.allclose(
        actual, (overlap / abs(overlap)) * matrix, atol=1e-8
    ):
        raise RuntimeError("Basis translation did not preserve the unitary.")

    return circuit


atexit.register(machine.finalize)
