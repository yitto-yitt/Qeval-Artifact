# EVAL_META: task_id=108, framework=cirq, class=3
import cirq
import numpy as np


def choi_to_kraus(choi_matrix, d_in, d_out):
    eigenvalues, eigenvectors = np.linalg.eigh(choi_matrix)
    kraus = []
    for val, vec in zip(eigenvalues, eigenvectors.T):
        if val > 1e-9:
            M = vec.reshape((d_in, d_out))
            A = np.sqrt(val) * M.T
            kraus.append(A)
    return kraus


def kraus_to_choi(kraus, d_in, d_out):
    J = np.zeros((d_in * d_out, d_in * d_out), dtype=complex)
    for A in kraus:
        vec = A.T.flatten()
        J += np.outer(vec, vec.conj())
    return J


def compose_kraus(kraus1, kraus2):
    composed = []
    for B in kraus2:
        for A in kraus1:
            composed.append(B @ A)
    return composed


class Choi(cirq.Choi):

    def __init__(self, data, input_tensor_shape=None, output_tensor_shape=None):
        if isinstance(data, cirq.Choi):
            matrix = data._matrix
            input_tensor_shape = data.input_tensor_shape
            output_tensor_shape = data.output_tensor_shape
        elif isinstance(data, np.ndarray):
            matrix = data
        else:
            matrix = np.array(data)

        N = matrix.shape[0]
        if input_tensor_shape is None or output_tensor_shape is None:
            d = int(np.sqrt(N))
            input_tensor_shape = (d,)
            output_tensor_shape = (d,)

        super().__init__(
            matrix=matrix,
            input_tensor_shape=input_tensor_shape,
            output_tensor_shape=output_tensor_shape,
        )

    def adjoint(self):
        d_in = np.prod(self.input_tensor_shape)
        d_out = np.prod(self.output_tensor_shape)

        reshaped = self._matrix.reshape((d_in, d_out, d_in, d_out))
        adjoint_reshaped = np.transpose(reshaped, (1, 0, 3, 2)).conj()
        adjoint_matrix = adjoint_reshaped.reshape((d_out * d_in, d_out * d_in))

        return Choi(
            adjoint_matrix,
            input_tensor_shape=self.output_tensor_shape,
            output_tensor_shape=self.input_tensor_shape,
        )

    def compose(self, other):
        if not isinstance(other, Choi):
            other = Choi(other)

        d_in1 = np.prod(self.input_tensor_shape)
        d_out1 = np.prod(self.output_tensor_shape)
        d_in2 = np.prod(other.input_tensor_shape)
        d_out2 = np.prod(other.output_tensor_shape)

        kraus1 = choi_to_kraus(self._matrix, d_in1, d_out1)
        kraus2 = choi_to_kraus(other._matrix, d_in2, d_out2)

        composed_kraus = compose_kraus(kraus1, kraus2)
        composed_matrix = kraus_to_choi(composed_kraus, d_in1, d_out2)

        return Choi(
            composed_matrix,
            input_tensor_shape=self.input_tensor_shape,
            output_tensor_shape=other.output_tensor_shape,
        )


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
