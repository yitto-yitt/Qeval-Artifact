# EVAL_META: task_id=86, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, Qubit, H, QGate

def collect_linear_blocks_with_and_without_limit():
    def compute_chain_matrix(n, ops):
        dim = 1 << n
        mat = np.zeros((dim, dim), dtype=complex)
        for i in range(dim):
            state = i
            for op in ops:
                if op[0] == 'CX':
                    _, c, t = op
                    if (state >> c) & 1:
                        state ^= (1 << t)
            mat[state, i] = 1
        return mat

    qubits = [Qubit(i) for i in range(5)]

    # Full block circuit
    full_circuit = QCircuit()
    full_circuit << H(qubits[0])
    ops_full = [('CX', 0, 1), ('CX', 1, 2), ('CX', 2, 3), ('CX', 3, 4)]
    mat_full = compute_chain_matrix(5, ops_full)
    full_circuit << QGate(mat_full, qubits)

    # Limited block circuit (max_block_width = 3)
    limited_circuit = QCircuit()
    limited_circuit << H(qubits[0])
    ops_block = [('CX', 0, 1), ('CX', 1, 2)]
    mat_block = compute_chain_matrix(3, ops_block)
    limited_circuit << QGate(mat_block, [qubits[0], qubits[1], qubits[2]])
    limited_circuit << QGate(mat_block, [qubits[2], qubits[3], qubits[4]])

    return full_circuit, limited_circuit
