# EVAL_META: task_id=108, framework=qpanda2, class=3
import atexit
import math
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)
atexit.register(machine.finalize)


def initialize_adjoint_and_compose(data1, data2):
    def as_choi_array(data):
        if hasattr(data, "data") and not isinstance(data, np.ndarray):
            data = data.data
        array = np.asarray(data, dtype=np.complex128)
        if array.ndim != 2 or array.shape[0] != array.shape[1]:
            raise ValueError("A Choi matrix must be square.")
        dimension = math.isqrt(array.shape[0])
        if dimension == 0 or dimension * dimension != array.shape[0]:
            raise ValueError("Cannot infer equal input and output dimensions.")
        return array, dimension

    array1, dimension1 = as_choi_array(data1)
    array2, dimension2 = as_choi_array(data2)
    if dimension1 != dimension2:
        raise ValueError("The channel dimensions are incompatible for composition.")

    dimension = dimension1
    bits = (dimension - 1).bit_length()
    side = 1 << bits
    if 4 * bits > len(qubits):
        raise ValueError("The Choi matrix exceeds the available quantum register.")

    def execute(amplitudes, program):
        state = np.zeros(1 << len(qubits), dtype=np.complex128)
        amplitudes = np.asarray(amplitudes, dtype=np.complex128).reshape(-1)
        norm = float(np.linalg.norm(amplitudes))
        if norm:
            state[:amplitudes.size] = amplitudes / norm
        else:
            state[0] = 1.0
        machine.init_state(state.tolist())
        program << pq.I(qubits[-1])
        machine.directly_run(program)
        return np.asarray(machine.get_qstate(), dtype=np.complex128), norm

    padded1 = np.zeros((side, side, side, side), dtype=np.complex128)
    padded2 = np.zeros_like(padded1)
    region = (slice(0, dimension),) * 4
    padded1[region] = array1.reshape((dimension,) * 4)
    padded2[region] = array2.reshape((dimension,) * 4)

    state, norm = execute(padded1, pq.QProg())
    choi1 = (
        state[:side ** 4].reshape((side,) * 4)[region]
        .reshape(array1.shape).copy() * norm
    )

    adjoint_program = pq.QProg()
    for bit in range(bits):
        adjoint_program << pq.SWAP(qubits[bit], qubits[bits + bit])
        adjoint_program << pq.SWAP(
            qubits[2 * bits + bit], qubits[3 * bits + bit]
        )
    state, norm = execute(padded1.conjugate(), adjoint_program)
    adjoint_choi1 = (
        state[:side ** 4].reshape((side,) * 4)[region]
        .reshape(array1.shape).copy() * norm
    )

    if 8 * bits <= len(qubits):
        composition_program = pq.QProg()
        for bit in range(bits):
            composition_program << pq.CNOT(
                qubits[6 * bits + bit], qubits[3 * bits + bit]
            )
            composition_program << pq.CNOT(
                qubits[4 * bits + bit], qubits[bits + bit]
            )
            composition_program << pq.H(qubits[6 * bits + bit])
            composition_program << pq.H(qubits[4 * bits + bit])

        product_state = np.kron(padded1.reshape(-1), padded2.reshape(-1))
        state, norm = execute(product_state, composition_program)
        contracted = state[:side ** 8].reshape((side,) * 8)[
            :, 0, :, 0, 0, :, 0, :
        ]
        composed_choi = (
            contracted.transpose(0, 2, 1, 3)[region]
            .reshape(array1.shape).copy() * (norm * side)
        )
    else:
        contraction_program = pq.QProg()
        for bit in range(2 * bits):
            contraction_program << pq.CNOT(
                qubits[2 * bits + bit], qubits[bit]
            )
            contraction_program << pq.H(qubits[2 * bits + bit])

        composed_tensor = np.empty((dimension,) * 4, dtype=np.complex128)
        for i in range(dimension):
            for j in range(dimension):
                first = padded1[i, :, j, :].reshape(-1)
                for c in range(dimension):
                    for d in range(dimension):
                        second = padded2[:, c, :, d].reshape(-1)
                        state, norm = execute(
                            np.kron(first, second), contraction_program
                        )
                        composed_tensor[i, c, j, d] = state[0] * norm * side
        composed_choi = composed_tensor.reshape(array1.shape)

    return choi1, adjoint_choi1, composed_choi
