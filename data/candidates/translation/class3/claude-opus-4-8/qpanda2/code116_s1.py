# EVAL_META: task_id=116, framework=qpanda2, class=3
import numpy as np
from scipy.linalg import expm
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(12)

_PAULI = {
    'I': np.array([[1, 0], [0, 1]], dtype=complex),
    'X': np.array([[0, 1], [1, 0]], dtype=complex),
    'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
    'Z': np.array([[1, 0], [0, -1]], dtype=complex),
}


def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    mat = np.array([[1.0 + 0j]])
    for ch in pauli_string:
        mat = np.kron(mat, _PAULI[ch])
    u = expm(-1j * time * mat)

    used = qubits[:n]
    prog = pq.QProg()
    prog << pq.QOracle(used, u)
    return prog


if __name__ == "__main__":
    p = synthesize_evolution_gate("XZ", 0.5)
    print(p)
    machine.finalize()
