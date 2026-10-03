# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def compose_op():
    matrices = []
    for gate in (pq.Y(2), pq.I(1), pq.X(0)):
        matrix = None
        for name in ("get_matrix", "matrix", "get_unitary", "unitary"):
            accessor = getattr(gate, name, None)
            if accessor is not None:
                value = accessor() if callable(accessor) else accessor
                matrix = np.asarray(value, dtype=complex).reshape(2, 2)
                break

        if matrix is None:
            circuit = pq.QCircuit()
            circuit << gate
            for name in ("get_matrix", "get_unitary"):
                accessor = getattr(pq, name, None)
                if callable(accessor):
                    matrix = np.asarray(accessor(circuit), dtype=complex).reshape(2, 2)
                    break

        if matrix is None:
            raise RuntimeError("The framework did not expose a gate matrix.")
        matrices.append(matrix)

    return np.kron(matrices[0], np.kron(matrices[1], matrices[2]))
