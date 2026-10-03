# EVAL_META: task_id=86, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    def compute_cx_chain_matrix(n, gates):
        dim = 2**n
        total = np.eye(dim, dtype=complex)
        for c, t in gates:
            mat = np.zeros((dim, dim), dtype=complex)
            for i in range(dim):
                if (i >> c) & 1:
                    j = i ^ (1 << t)
                else:
                    j = i
                mat[j, i] = 1.0
            total = mat @ total
        return total

    # Full block: all 5 qubits, CX chain (0,1), (1,2), (2,3), (3,4)
    # qubit order: q0, q1, q2, q3, q4 -> local bits: 4,3,2,1,0
    full_gates = [(4, 3), (3, 2), (2, 1), (1, 0)]
    full_matrix = compute_cx_chain_matrix(5, full_gates)

    # Limited block: max width 3
    # Block on q0,q1,q2: local bits 2,1,0 -> gates (2,1), (1,0)
    block_gates = [(2, 1), (1, 0)]
    block_matrix = compute_cx_chain_matrix(3, block_gates)

    full_circuit = QProg()
    full_circuit << H(qubits[0])
    full_circuit << QOracle(qubits, full_matrix)

    limited_circuit = QProg()
    limited_circuit << H(qubits[0])
    limited_circuit << QOracle([qubits[0], qubits[1], qubits[2]], block_matrix)
    limited_circuit << QOracle([qubits[2], qubits[3], qubits[4]], block_matrix)

    return full_circuit, limited_circuit

if __name__ == "__main__":
    machine.finalize()
