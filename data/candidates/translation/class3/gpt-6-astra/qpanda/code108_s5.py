# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def initialize_adjoint_and_compose(data1, data2):
    def as_choi(data):
        if not isinstance(data, (np.ndarray, list, tuple)) and hasattr(data, "data"):
            data = data.data
        matrix = np.asarray(data, dtype=complex)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Choi data must be a square matrix.")
        dim = int(round(np.sqrt(matrix.shape[0])))
        if dim * dim != matrix.shape[0]:
            raise ValueError("Cannot infer equal input and output dimensions.")
        return matrix, dim

    choi1, dim1 = as_choi(data1)
    choi2, dim2 = as_choi(data2)
    if dim1 != dim2:
        raise ValueError("The channel dimensions do not match.")

    dim = dim1
    size = dim * dim
    padded_size = 1 << (size - 1).bit_length()

    def block_encoding(choi):
        superoperator = choi.reshape(dim, dim, dim, dim).transpose(
            1, 3, 0, 2
        ).reshape(size, size)
        padded = np.zeros((padded_size, padded_size), dtype=complex)
        padded[:size, :size] = superoperator
        left, singular, right = np.linalg.svd(padded, full_matrices=True)
        scale = max(1.0, float(singular[0]))
        contraction = padded / scale
        roots = np.sqrt(np.maximum(0.0, 1.0 - (singular / scale) ** 2))
        upper_right = (left * roots) @ left.conj().T
        lower_left = (right.conj().T * roots) @ right
        unitary = np.block([
            [contraction, upper_right],
            [lower_left, -contraction.conj().T],
        ])
        return unitary, scale

    unitary1, scale1 = block_encoding(choi1)
    unitary2, scale2 = block_encoding(choi2)

    full1 = np.kron(np.eye(2, dtype=complex), unitary1)
    full2 = np.einsum(
        "axby,cd->acxbdy",
        unitary2.reshape(2, padded_size, 2, padded_size),
        np.eye(2, dtype=complex),
    ).reshape(4 * padded_size, 4 * padded_size)

    total_size = full1.shape[0]
    num_qubits = total_size.bit_length() - 1
    qubits = list(range(num_qubits))

    def oracle(matrix):
        errors = []
        for representation in (matrix, matrix.tolist(), matrix.ravel().tolist()):
            try:
                return pq.QOracle(qubits, representation)
            except (TypeError, ValueError, RuntimeError) as error:
                errors.append(error)
        raise errors[-1]

    def build(matrices, container_type):
        program = container_type()
        for matrix in matrices:
            program << oracle(matrix)
        return program

    containers = [pq.QProg]
    if hasattr(pq, "QCircuit"):
        containers.append(pq.QCircuit)

    extractors = []
    for name in ("get_matrix", "get_unitary"):
        operation = getattr(pq, name, None)
        if callable(operation):
            extractors.append(lambda program, operation=operation: operation(program))
        extractors.append(
            lambda program, name=name: getattr(program, name)()
        )

    reverse = np.array([
        int(format(index, "0{}b".format(num_qubits))[::-1], 2)
        for index in range(total_size)
    ])

    selected = None
    last_error = None
    for container_type in containers:
        if selected is not None:
            break
        for extract in extractors:
            try:
                extracted1 = np.asarray(
                    extract(build([full1], container_type)), dtype=complex
                ).reshape(total_size, total_size)
                extracted2 = np.asarray(
                    extract(build([full2], container_type)), dtype=complex
                ).reshape(total_size, total_size)
                for indices in (np.arange(total_size), reverse):
                    test1 = extracted1[np.ix_(indices, indices)]
                    test2 = extracted2[np.ix_(indices, indices)]
                    if (
                        np.allclose(test1, full1, atol=1e-8, rtol=1e-8)
                        and np.allclose(test2, full2, atol=1e-8, rtol=1e-8)
                    ):
                        selected = (container_type, extract, indices, test1)
                        break
                if selected is not None:
                    break
            except (AttributeError, TypeError, ValueError, RuntimeError) as error:
                last_error = error

    if selected is None:
        raise RuntimeError(
            "The framework could not extract the oracle program's unitary."
        ) from last_error

    container_type, extract, indices, extracted1 = selected

    def framework_matrix(matrices):
        result = np.asarray(
            extract(build(matrices, container_type)), dtype=complex
        ).reshape(total_size, total_size)
        return result[np.ix_(indices, indices)]

    adjoint_unitary = framework_matrix([full1.conj().T])
    composed_unitary = framework_matrix([full1, full2])

    def to_choi(encoded, scale):
        superoperator = encoded[:size, :size] * scale
        return superoperator.reshape(dim, dim, dim, dim).transpose(
            2, 0, 3, 1
        ).reshape(size, size).copy()

    return (
        to_choi(extracted1, scale1),
        to_choi(adjoint_unitary, scale1),
        to_choi(composed_unitary, scale1 * scale2),
    )
