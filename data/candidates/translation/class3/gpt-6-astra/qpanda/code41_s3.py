# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3 import core


def compose_op():
    def gate_matrix(gate):
        names = ("matrix", "get_matrix", "gate_matrix", "get_unitary", "unitary")
        for obj in (gate, core.QProg([gate])):
            for name in names:
                member = getattr(obj, name, None)
                if member is None:
                    continue
                try:
                    value = member() if callable(member) else member
                    matrix = np.asarray(value, dtype=complex)
                    if matrix.size == 4:
                        return matrix.reshape(2, 2)
                except (TypeError, ValueError, RuntimeError):
                    continue
            for name in names:
                function = getattr(core, name, None)
                if not callable(function):
                    continue
                try:
                    matrix = np.asarray(function(obj), dtype=complex)
                    if matrix.size == 4:
                        return matrix.reshape(2, 2)
                except (TypeError, ValueError, RuntimeError):
                    continue
        raise RuntimeError("Unable to extract a gate matrix from pyqpanda3.")

    x = gate_matrix(core.X(0))
    y = gate_matrix(core.Y(0))
    identity = np.eye(8, dtype=complex)
    embedded_yx = np.kron(y, np.kron(np.eye(2, dtype=complex), x))
    return identity @ embedded_yx
