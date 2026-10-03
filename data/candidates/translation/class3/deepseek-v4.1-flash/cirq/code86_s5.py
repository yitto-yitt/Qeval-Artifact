# EVAL_META: task_id=86, framework=cirq, class=3
import cirq
import numpy as np

def collect_linear_blocks_with_and_without_limit():
    def linear_function_matrix(mat):
        n = len(mat)
        dim = 2**n
        U = np.zeros((dim, dim), dtype=complex)
        for x in range(dim):
            y = 0
            for i in range(n):
                bit = 0
                for j in range(n):
                    if mat[i][j]:
                        bit ^= (x >> (n - 1 - j)) & 1
                y |= bit << (n - 1 - i)
            U[y, x] = 1.0
        return U

    q = cirq.LineQubit.range(5)
    M5 = [
        [1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1]
    ]
    U5 = linear_function_matrix(M5)
    full_block = cirq.Circuit()
    full_block.append(cirq.H(q[0]))
    full_block.append(cirq.MatrixGate(U5).on(*q))
    
    M3 = [
        [1, 0, 0],
        [1, 1, 0],
        [1, 1, 1]
    ]
    U3 = linear_function_matrix(M3)
    limited_block = cirq.Circuit()
    limited_block.append(cirq.H(q[0]))
    limited_block.append(cirq.MatrixGate(U3).on(q[0], q[1], q[2]))
    limited_block.append(cirq.MatrixGate(U3).on(q[2], q[3], q[4]))
    
    return full_block, limited_block
