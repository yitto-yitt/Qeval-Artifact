# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def initialize_adjoint_and_compose(data1, data2):
    try:
        native_choi = getattr(pq, "Choi")
        choi1 = native_choi(data1)
        choi2 = native_choi(data2)
        return choi1, choi1.adjoint(), choi1.compose(choi2)
    except Exception:
        pass

    class _Choi:
        __array_priority__ = 1000

        def __init__(self, data):
            if isinstance(data, _Choi):
                self._data = np.array(data.data, dtype=complex, copy=True)
                self._input_dims = tuple(data.input_dims())
                self._output_dims = tuple(data.output_dims())
                self._input_dim = int(np.prod(self._input_dims, dtype=int))
                self._output_dim = int(np.prod(self._output_dims, dtype=int))
                return

            arr_source = data
            in_dims = None
            out_dims = None

            if not isinstance(data, (np.ndarray, np.matrix, list, tuple)):
                data_attr = getattr(data, "data", None)
                if data_attr is not None:
                    arr_source = data_attr

                input_dims_attr = getattr(data, "input_dims", None)
                output_dims_attr = getattr(data, "output_dims", None)
                try:
                    in_dims = input_dims_attr() if callable(input_dims_attr) else input_dims_attr
                    out_dims = output_dims_attr() if callable(output_dims_attr) else output_dims_attr
                except Exception:
                    in_dims = None
                    out_dims = None

            arr = np.asarray(arr_source, dtype=complex)
            if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
                raise ValueError("Choi data must be a square matrix.")

            if in_dims is None or out_dims is None:
                root = int(round(np.sqrt(arr.shape[0])))
                if root * root != arr.shape[0]:
                    raise ValueError("Cannot infer input and output dimensions from Choi data.")
                in_dims = self._auto_dims(root)
                out_dims = self._auto_dims(root)
            else:
                in_dims = self._normalize_dims(in_dims)
                out_dims = self._normalize_dims(out_dims)

            input_dim = int(np.prod(in_dims, dtype=int))
            output_dim = int(np.prod(out_dims, dtype=int))
            if input_dim * output_dim != arr.shape[0]:
                raise ValueError("Input and output dimensions are incompatible with Choi data.")

            self._data = np.array(arr, dtype=complex, copy=True)
            self._input_dims = tuple(in_dims)
            self._output_dims = tuple(out_dims)
            self._input_dim = input_dim
            self._output_dim = output_dim

        @staticmethod
        def _normalize_dims(dims):
            if dims is None:
                return None
            if isinstance(dims, (int, np.integer)):
                return (int(dims),)
            return tuple(int(d) for d in dims)

        @staticmethod
        def _auto_dims(dim):
            dim = int(dim)
            if dim == 1:
                return (1,)
            if dim > 0 and (dim & (dim - 1)) == 0:
                return (2,) * int(np.log2(dim))
            return (dim,)

        @classmethod
        def _from_superop(cls, superop, input_dim, output_dim):
            obj = cls.__new__(cls)
            input_dim = int(input_dim)
            output_dim = int(output_dim)
            obj._input_dim = input_dim
            obj._output_dim = output_dim
            obj._input_dims = cls._auto_dims(input_dim)
            obj._output_dims = cls._auto_dims(output_dim)
            obj._data = np.asarray(superop, dtype=complex).reshape(
                output_dim, output_dim, input_dim, input_dim
            ).transpose(0, 2, 1, 3).reshape(output_dim * input_dim, output_dim * input_dim)
            return obj

        @property
        def data(self):
            return self._data

        @data.setter
        def data(self, value):
            arr = np.asarray(value, dtype=complex)
            if arr.shape != self._data.shape:
                raise ValueError("New data must have the same shape.")
            self._data = np.array(arr, dtype=complex, copy=True)

        @property
        def dim(self):
            return self._input_dim, self._output_dim

        def input_dims(self, qargs=None):
            if qargs is not None:
                return tuple(self._input_dims[i] for i in qargs)
            return self._input_dims

        def output_dims(self, qargs=None):
            if qargs is not None:
                return tuple(self._output_dims[i] for i in qargs)
            return self._output_dims

        def copy(self):
            return _Choi(self)

        def to_matrix(self):
            return np.array(self._data, dtype=complex, copy=True)

        def _to_superop(self):
            return self._data.reshape(
                self._output_dim, self._input_dim, self._output_dim, self._input_dim
            ).transpose(0, 2, 1, 3).reshape(
                self._output_dim * self._output_dim,
                self._input_dim * self._input_dim,
            )

        def adjoint(self):
            return _Choi._from_superop(
                self._to_superop().conjugate().T,
                self._output_dim,
                self._input_dim,
            )

        def compose(self, other, qargs=None, front=False):
            if qargs is not None:
                raise NotImplementedError("Subsystem composition is not implemented.")
            other = _Choi(other)
            if front:
                return other.compose(self)

            if self._input_dim != other._output_dim:
                raise ValueError("Channel dimensions are not compatible for composition.")

            superop = self._to_superop() @ other._to_superop()
            return _Choi._from_superop(superop, other._input_dim, self._output_dim)

        def __array__(self, dtype=None, copy=None):
            arr = np.asarray(self._data, dtype=dtype)
            if copy:
                arr = arr.copy()
            return arr

        def __repr__(self):
            return f"Choi({self._data!r}, input_dims={self._input_dims}, output_dims={self._output_dims})"

    choi1 = _Choi(data1)
    choi2 = _Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
