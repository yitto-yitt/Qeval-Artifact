# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def compose_op():
    def gate_matrix(gate):
        for name in ("get_matrix", "matrix", "get_unitary"):
            accessor = getattr(gate, name, None)
            if accessor is not None:
                value = accessor() if callable(accessor) else accessor
                return np.asarray(value, dtype=complex).reshape(2, 2)

        circuit = pq.QCircuit()
        circuit << gate
        for name in ("get_matrix", "matrix", "get_unitary"):
            accessor = getattr(circuit, name, None)
            if accessor is not None:
                value = accessor() if callable(accessor) else accessor
                return np.asarray(value, dtype=complex).reshape(2, 2)

        return np.asarray(pq.get_matrix(circuit), dtype=complex).reshape(2, 2)

    x = gate_matrix(pq.X(0))
    identity = gate_matrix(pq.I(0))
    y = gate_matrix(pq.Y(0))
    return np.kron(y, np.kron(identity, x))
