# EVAL_META: task_id=116, framework=qpanda2, class=3
import numpy as np
from scipy.linalg import expm
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(12)

def synthesize_evolution_gate(pauli_string, time):
    I = np.array([[1, 0], [0, 1]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    pmap = {'I': I, 'X': X, 'Y': Y, 'Z': Z}

    n = len(pauli_string)
    # Qiskit Pauli string is little-endian: rightmost char is qubit 0
    mat = None
    for ch in pauli_string:
        m = pmap[ch]
        mat = m if mat is None else np.kron(mat, m)

    U = expm(-1j * time * mat)

    qs = qubits[:n]
    prog = pq.QProg()
    prog << pq.matrix_decompose(qs, U)

    machine.directly_run(prog)
    return prog

if __name__ == "__main__":
    synthesize_evolution_gate("XZ", 0.5)
    machine.finalize()
