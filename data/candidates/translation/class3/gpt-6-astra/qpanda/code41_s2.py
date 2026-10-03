# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def compose_op():
    def operator_matrix(gates):
        for container_type in (pq.QCircuit, pq.QProg):
            program = container_type()
            for gate in gates:
                program << gate

            for name in ("get_matrix", "get_unitary", "matrix", "unitary"):
                method = getattr(program, name, None)
                if method is not None:
                    try:
                        value = method() if callable(method) else method
                        matrix = np.asarray(value, dtype=complex)
                        if matrix.size == 64:
                            return matrix.reshape(8, 8)
                    except (TypeError, ValueError, RuntimeError):
                        pass

                function = getattr(pq, name, None)
                if callable(function):
                    try:
                        matrix = np.asarray(function(program), dtype=complex)
                        if matrix.size == 64:
                            return matrix.reshape(8, 8)
                    except (TypeError, ValueError, RuntimeError):
                        pass

        raise RuntimeError("No supported framework operator-matrix interface found.")

    identity = [pq.I(0), pq.I(1), pq.I(2)]
    matrix = operator_matrix(identity + [pq.X(0), pq.Y(2)])
    ordering_probe = operator_matrix(
        [pq.I(0), pq.I(1), pq.I(2), pq.X(0)]
    )

    if int(np.argmax(np.abs(ordering_probe[:, 0]))) == 4:
        permutation = [
            ((index & 1) << 2) | (index & 2) | ((index & 4) >> 2)
            for index in range(8)
        ]
        matrix = matrix[np.ix_(permutation, permutation)]

    return matrix
