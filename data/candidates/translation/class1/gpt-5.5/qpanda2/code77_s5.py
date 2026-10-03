# EVAL_META: task_id=77, framework=qpanda2, class=1
import math
import numpy as np
from pyqpanda import CPUQVM, QCircuit, I, matrix_decompose


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    dim = 1 << num_qubits

    amplitudes = np.array(
        [math.sqrt(probability_dist.get(basis_state, 0)) for basis_state in range(dim)],
        dtype=np.complex128,
    )

    norm = np.linalg.norm(amplitudes)
    if norm == 0:
        raise ValueError("Amplitude vector has zero norm.")
    amplitudes = amplitudes / norm

    e0 = np.zeros(dim, dtype=np.complex128)
    e0[0] = 1.0

    if np.allclose(amplitudes, e0):
        unitary = np.eye(dim, dtype=np.complex128)
    else:
        householder = e0 - amplitudes
        householder = householder / np.linalg.norm(householder)
        unitary = np.eye(dim, dtype=np.complex128) - 2.0 * np.outer(
            householder, np.conjugate(householder)
        )

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(num_qubits)

    circuit = QCircuit()
    for qubit in qubits:
        circuit << I(qubit)
    circuit << matrix_decompose(qubits, unitary.tolist())

    if not hasattr(circuit_from_probability_dist, "_qvms"):
        circuit_from_probability_dist._qvms = []
    circuit_from_probability_dist._qvms.append(qvm)

    return circuit
