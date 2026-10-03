# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def initialize_adjoint_and_compose(data1, data2):
    class Choi:
        def __init__(self, data, input_dims=None, output_dims=None):
            if isinstance(data, Choi):
                self.data = np.array(data.data, dtype=complex, copy=True)
                self._input_dims = tuple(data._input_dims)
                self._output_dims = tuple(data._output_dims)
                return

            if input_dims is None and hasattr(data, "input_dims"):
                try:
                    input_dims = tuple(data.input_dims())
                except TypeError:
                    input_dims = tuple(data.input_dims)
            if output_dims is None and hasattr(data, "output_dims"):
                try:
                    output_dims = tuple(data.output_dims())
                except TypeError:
                    output_dims = tuple(data.output_dims)

            raw = data
            if not isinstance(raw, np.ndarray) and hasattr(raw, "data"):
                raw = raw.data
            elif hasattr(raw, "to_matrix"):
                raw = raw.to_matrix()

            arr = np.asarray(raw, dtype=complex)
            if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
                raise ValueError("Choi data must be a square matrix")

            dim = int(arr.shape[0])

            if input_dims is None or output_dims is None:
                root = int(round(np.sqrt(dim)))
                if root * root == dim:
                    inferred_input = (root,)
                    inferred_output = (root,)
                else:
                    inferred_input = (1,)
                    inferred_output = (dim,)
                if input_dims is None:
                    input_dims = inferred_input
                if output_dims is None:
                    output_dims = inferred_output

            self._input_dims = tuple(int(x) for x in input_dims)
            self._output_dims = tuple(int(x) for x in output_dims)

            if int(np.prod(self._input_dims)) * int(np.prod(self._output_dims)) != dim:
                raise ValueError("Input and output dimensions do not match Choi matrix size")

            self.data = np.array(arr, dtype=complex, copy=True)

        @property
        def dim(self):
            return int(np.prod(self._input_dims)), int(np.prod(self._output_dims))

        def input_dims(self):
            return self._input_dims

        def output_dims(self):
            return self._output_dims

        def copy(self):
            return Choi(self)

        def adjoint(self):
            input_dim = int(np.prod(self._input_dims))
            output_dim = int(np.prod(self._output_dims))
            tensor = self.data.reshape(output_dim, input_dim, output_dim, input_dim)
            adj_data = np.conjugate(np.transpose(tensor, (1, 0, 3, 2))).reshape(
                input_dim * output_dim, input_dim * output_dim
            )
            return Choi(adj_data, input_dims=self._output_dims, output_dims=self._input_dims)

        def compose(self, other, qargs=None, front=False):
            if qargs is not None:
                raise NotImplementedError("Subsystem composition is not implemented for this Choi translation")

            other = Choi(other)

            def compose_pair(first, second):
                first_input_dim = int(np.prod(first._input_dims))
                first_output_dim = int(np.prod(first._output_dims))
                second_input_dim = int(np.prod(second._input_dims))
                second_output_dim = int(np.prod(second._output_dims))

                if first_output_dim != second_input_dim:
                    raise ValueError("Output dimension of first channel must match input dimension of second channel")

                first_tensor = first.data.reshape(
                    first_output_dim, first_input_dim, first_output_dim, first_input_dim
                )
                second_tensor = second.data.reshape(
                    second_output_dim, second_input_dim, second_output_dim, second_input_dim
                )
                result_tensor = np.einsum("cadb,ambn->cmdn", second_tensor, first_tensor)
                result_data = result_tensor.reshape(
                    second_output_dim * first_input_dim, second_output_dim * first_input_dim
                )
                return Choi(result_data, input_dims=first._input_dims, output_dims=second._output_dims)

            if front:
                return compose_pair(other, self)
            return compose_pair(self, other)

        def __array__(self, dtype=None):
            return np.asarray(self.data, dtype=dtype)

        def __repr__(self):
            return f"Choi({repr(self.data)})"

    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi


machine.finalize()
