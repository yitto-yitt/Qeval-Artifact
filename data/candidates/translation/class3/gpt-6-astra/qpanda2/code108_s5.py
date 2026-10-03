# EVAL_META: task_id=108, framework=qpanda2, class=3
import atexit
import math
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(12)


def initialize_adjoint_and_compose(data1, data2):
    def as_choi(data):
        matrix = np.asarray(data, dtype=np.complex128)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("A Choi matrix must be square.")
        dimension = math.isqrt(matrix.shape[0])
        if dimension == 0 or dimension * dimension != matrix.shape[0]:
            raise ValueError("Cannot infer equal input and output dimensions.")
        return matrix, dimension

    choi1, dimension1 = as_choi(data1)
    choi2, dimension2 = as_choi(data2)
    if dimension1 != dimension2:
        raise ValueError("The channel dimensions are incompatible.")

    dimension = dimension1
    size = dimension * dimension
    register_size = (size - 1).bit_length()
    padded_size = 1 << register_size
    if register_size + 2 > len(qubits):
        raise ValueError("The channel exceeds the allocated quantum register.")

    def reshuffle(matrix):
        return (
            matrix.reshape(dimension, dimension, dimension, dimension)
            .transpose(3, 1, 2, 0)
            .reshape(size, size)
        )

    def dilation(matrix):
        padded = np.zeros((padded_size, padded_size), dtype=np.complex128)
        padded[:size, :size] = matrix
        left, singular_values, right_h = np.linalg.svd(padded)
        scale = max(1.0, float(singular_values[0]))
        singular_values = np.clip(singular_values / scale, 0.0, 1.0)
        complement = np.sqrt(np.maximum(0.0, 1.0 - singular_values**2))
        right = right_h.conj().T
        contraction = (left * singular_values) @ right_h
        unitary = np.block(
            [
                [
                    contraction,
                    (left * complement) @ left.conj().T,
                ],
                [
                    (right * complement) @ right_h,
                    -contraction.conj().T,
                ],
            ]
        )
        return unitary, scale

    unitary1, scale1 = dilation(reshuffle(choi1))
    unitary2, scale2 = dilation(reshuffle(choi2))

    system_qubits = list(qubits[:register_size])
    gate1 = pq.QOracle(
        system_qubits + [qubits[register_size]],
        unitary1.ravel().tolist(),
    )
    gate2 = pq.QOracle(
        system_qubits + [qubits[register_size + 1]],
        unitary2.ravel().tolist(),
    )

    initial_state = np.zeros(1 << len(qubits), dtype=np.complex128)
    initial_state[0] = 1.0
    initial_state = initial_state.tolist()

    def projected_matrix(gates, scale):
        result = np.empty((size, size), dtype=np.complex128)
        for column in range(size):
            machine.init_state(initial_state)
            program = pq.QProg()
            for bit in range(register_size):
                if column & (1 << bit):
                    program << pq.X(qubits[bit])
            for gate in gates:
                program << gate
            machine.directly_run(program)
            state = np.asarray(machine.get_qstate(), dtype=np.complex128)
            result[:, column] = scale * state[:size]
        return result

    original = projected_matrix([gate1], scale1)
    adjoint = projected_matrix([gate1.dagger()], scale1)
    composed = projected_matrix([gate1, gate2], scale1 * scale2)

    return reshuffle(original), reshuffle(adjoint), reshuffle(composed)


atexit.register(lambda: machine.finalize())
