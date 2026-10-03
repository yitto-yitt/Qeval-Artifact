# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq
from qiskit.quantum_info import Choi


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)

    input1 = int(np.prod(choi1.input_dims()))
    output1 = int(np.prod(choi1.output_dims()))
    input2 = int(np.prod(choi2.input_dims()))
    output2 = int(np.prod(choi2.output_dims()))

    if choi1.output_dims() != choi2.input_dims():
        raise ValueError("Channel dimensions are incompatible for composition.")

    super1 = (
        np.asarray(choi1.data, dtype=complex)
        .reshape(input1, output1, input1, output1)
        .transpose(1, 3, 0, 2)
        .reshape(output1 ** 2, input1 ** 2)
    )
    super2 = (
        np.asarray(choi2.data, dtype=complex)
        .reshape(input2, output2, input2, output2)
        .transpose(1, 3, 0, 2)
        .reshape(output2 ** 2, input2 ** 2)
    )

    size = max(*super1.shape, *super2.shape)
    size = 1 << (size - 1).bit_length()

    def dilate(matrix):
        padded = np.zeros((size, size), dtype=complex)
        padded[:matrix.shape[0], :matrix.shape[1]] = matrix
        left, singular, right_h = np.linalg.svd(padded)
        scale = max(1.0, float(singular[0]))
        contraction = padded / scale
        defect = np.sqrt(np.maximum(0.0, 1.0 - (singular / scale) ** 2))
        upper_right = (left * defect) @ left.conj().T
        lower_left = (right_h.conj().T * defect) @ right_h
        unitary = np.block([
            [contraction, upper_right],
            [lower_left, -contraction.conj().T],
        ])
        return unitary, scale

    def unitary_circuit(matrix):
        qubits = list(range(matrix.shape[0].bit_length() - 1))
        circuit = pq.QCircuit()
        if hasattr(pq, "QOracle"):
            circuit << pq.QOracle(qubits, matrix)
        else:
            circuit << pq.matrix_decompose(qubits, matrix)
        return circuit

    def circuit_matrix(circuit, dimension):
        for name in ("get_matrix", "get_unitary", "get_unitary_matrix"):
            method = getattr(circuit, name, None)
            if callable(method):
                try:
                    return np.asarray(method(), dtype=complex).reshape(
                        dimension, dimension
                    )
                except TypeError:
                    pass

            function = getattr(pq, name, None)
            if callable(function):
                try:
                    return np.asarray(function(circuit), dtype=complex).reshape(
                        dimension, dimension
                    )
                except TypeError:
                    pass

        program = pq.QProg()
        program << circuit
        for name in ("get_matrix", "get_unitary", "get_qprog_matrix"):
            function = getattr(pq, name, None)
            if callable(function):
                try:
                    return np.asarray(function(program), dtype=complex).reshape(
                        dimension, dimension
                    )
                except TypeError:
                    pass
        raise RuntimeError("No circuit-matrix extraction API is available.")

    unitary1, scale1 = dilate(super1)
    unitary2, scale2 = dilate(super2)

    adjoint_circuit = unitary_circuit(unitary1).dagger()
    adjoint_super = (
        circuit_matrix(adjoint_circuit, 2 * size)[
            :input1 ** 2, :output1 ** 2
        ]
        * scale1
    )

    first_unitary = np.kron(np.eye(2, dtype=complex), unitary1)
    second_unitary = np.einsum(
        "aibj,cd->acibdj",
        unitary2.reshape(2, size, 2, size),
        np.eye(2, dtype=complex),
    ).reshape(4 * size, 4 * size)

    composed_circuit = pq.QCircuit()
    composed_circuit << unitary_circuit(first_unitary)
    composed_circuit << unitary_circuit(second_unitary)
    composed_super = (
        circuit_matrix(composed_circuit, 4 * size)[
            :output2 ** 2, :input1 ** 2
        ]
        * scale1
        * scale2
    )

    adjoint_data = (
        adjoint_super.reshape(input1, input1, output1, output1)
        .transpose(2, 0, 3, 1)
        .reshape(output1 * input1, output1 * input1)
    )
    composed_data = (
        composed_super.reshape(output2, output2, input1, input1)
        .transpose(2, 0, 3, 1)
        .reshape(input1 * output2, input1 * output2)
    )

    adjoint_choi1 = Choi(
        adjoint_data,
        input_dims=choi1.output_dims(),
        output_dims=choi1.input_dims(),
    )
    composed_choi = Choi(
        composed_data,
        input_dims=choi1.input_dims(),
        output_dims=choi2.output_dims(),
    )
    return choi1, adjoint_choi1, composed_choi
