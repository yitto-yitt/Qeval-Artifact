# EVAL_META: task_id=117, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def decompose_unitary(unitary):
    if hasattr(unitary, "to_matrix"):
        matrix = np.asarray(unitary.to_matrix(), dtype=np.complex128)
    elif isinstance(unitary, np.ndarray):
        matrix = np.asarray(unitary, dtype=np.complex128)
    else:
        matrix = np.asarray(getattr(unitary, "data", unitary), dtype=np.complex128)

    if matrix.shape != (4, 4):
        raise ValueError("unitary must be a 4x4 matrix.")
    if not np.allclose(matrix.conj().T @ matrix, np.eye(4), atol=1e-10):
        raise ValueError("The input matrix must be unitary.")

    for ordered_qubits in (qubits, list(reversed(qubits))):
        circuit = pq.matrix_decompose(ordered_qubits, matrix)
        program = pq.QProg()
        program << circuit
        reconstructed = np.asarray(
            pq.get_matrix(program), dtype=np.complex128
        ).reshape(4, 4)
        overlap = np.vdot(matrix, reconstructed) / 4.0
        if abs(overlap) > 0 and np.allclose(
            reconstructed, matrix * overlap / abs(overlap), atol=1e-8
        ):
            break
    else:
        raise RuntimeError("Unable to match the input matrix's qubit ordering.")

    program = pq.transform_to_base_qgate(
        program, machine, ["U3"], ["CNOT"]
    )
    machine.directly_run(program)
    return pq.cast_qprog_qcircuit(program)


atexit.register(machine.finalize)
