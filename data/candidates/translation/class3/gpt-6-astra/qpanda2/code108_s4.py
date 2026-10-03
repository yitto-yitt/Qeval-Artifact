# EVAL_META: task_id=108, framework=qpanda2, class=3
import atexit
import math
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(12)


def initialize_adjoint_and_compose(data1, data2):
    def read_choi(data):
        if isinstance(data, (list, tuple, np.ndarray)):
            matrix = np.asarray(data, dtype=complex)
        else:
            matrix = np.asarray(data.data, dtype=complex)

        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Choi matrices must be square.")
        if matrix.shape[0] == 0 or not np.all(np.isfinite(matrix)):
            raise ValueError("Choi matrices must be nonempty and finite.")

        size = matrix.shape[0]
        if callable(getattr(data, "input_dims", None)):
            input_dim = math.prod(data.input_dims())
            output_dim = math.prod(data.output_dims())
        else:
            input_dim = math.isqrt(size)
            output_dim = size // input_dim

        if input_dim * output_dim != size:
            raise ValueError("Cannot infer valid channel dimensions.")

        superoperator = (
            matrix.reshape(input_dim, output_dim, input_dim, output_dim)
            .transpose(1, 3, 0, 2)
            .reshape(output_dim**2, input_dim**2)
        )
        return superoperator, input_dim, output_dim

    super1, input1, output1 = read_choi(data1)
    super2, input2, output2 = read_choi(data2)

    if output1 != input2:
        raise ValueError("The channel dimensions are incompatible for composition.")

    largest_dimension = max(*super1.shape, *super2.shape)
    system_width = max(1, (largest_dimension - 1).bit_length())
    if system_width + 2 > len(qubits):
        raise ValueError("The channel exceeds the allocated quantum register.")

    padded_dimension = 1 << system_width
    system_qubits = qubits[:system_width]

    def block_encode(operator, ancilla):
        padded = np.zeros(
            (padded_dimension, padded_dimension), dtype=complex
        )
        padded[: operator.shape[0], : operator.shape[1]] = operator

        left, singular_values, right_dagger = np.linalg.svd(padded)
        scale = max(1.0, float(singular_values[0]))
        complement = np.sqrt(
            np.maximum(0.0, 1.0 - (singular_values / scale) ** 2)
        )
        upper_right = (left * complement) @ left.conj().T
        right = right_dagger.conj().T
        lower_left = (right * complement) @ right_dagger

        unitary = np.block(
            [
                [padded / scale, upper_right],
                [lower_left, -padded.conj().T / scale],
            ]
        )
        gate = pq.QOracle(
            system_qubits + [ancilla],
            unitary.ravel().tolist(),
        )
        return gate, scale

    gate1, scale1 = block_encode(super1, qubits[system_width])
    gate2, scale2 = block_encode(super2, qubits[system_width + 1])

    def extract_block(gates, rows, columns, scale):
        result = np.empty((rows, columns), dtype=complex)
        for column in range(columns):
            program = pq.QProg()
            for bit, qubit in enumerate(system_qubits):
                if (column >> bit) & 1:
                    program << pq.X(qubit)
            for gate in gates:
                program << gate

            machine.directly_run(program)
            state = np.asarray(machine.get_qstate(), dtype=complex)
            result[:, column] = state[:rows] * scale
        return result

    initialized = extract_block(
        [gate1], output1**2, input1**2, scale1
    )
    adjoint = extract_block(
        [gate1.dagger()], input1**2, output1**2, scale1
    )
    composed = extract_block(
        [gate1, gate2], output2**2, input1**2, scale1 * scale2
    )

    def as_choi(superoperator, input_dim, output_dim):
        return (
            superoperator.reshape(output_dim, output_dim, input_dim, input_dim)
            .transpose(2, 0, 3, 1)
            .reshape(input_dim * output_dim, input_dim * output_dim)
        )

    return (
        as_choi(initialized, input1, output1),
        as_choi(adjoint, output1, input1),
        as_choi(composed, input1, output2),
    )


atexit.register(lambda: machine.finalize())
