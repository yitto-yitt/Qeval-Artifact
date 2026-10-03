# EVAL_META: task_id=125, framework=qpanda, class=3
import numpy as np
from pyqpanda3 import core


def circ_to_gate(circ):
    to_gate = getattr(circ, "to_gate", None)
    if callable(to_gate):
        return to_gate()

    def framework_value(method_names, function_names):
        for name in method_names:
            member = getattr(circ, name, None)
            if member is not None:
                try:
                    return member() if callable(member) else member
                except TypeError:
                    pass
        for name in function_names:
            function = getattr(core, name, None)
            if callable(function):
                try:
                    return function(circ)
                except TypeError:
                    pass
        raise TypeError("The circuit does not expose the required unitary information.")

    qubits = framework_value(
        ("get_used_qubits", "get_qubits", "get_all_used_qubits", "qubits"),
        ("get_all_used_qubits", "get_used_qubits"),
    )
    matrix = framework_value(
        ("get_matrix", "get_unitary", "matrix", "unitary"),
        ("get_matrix", "get_unitary"),
    )

    qubits = list(qubits)
    matrix = np.asarray(matrix, dtype=complex)
    dimension = 1 << len(qubits)
    matrix = matrix.reshape(dimension, dimension)

    last_error = None
    for name in ("QOracle", "Oracle", "QGate"):
        constructor = getattr(core, name, None)
        if not callable(constructor):
            continue
        for representation in (
            matrix,
            matrix.tolist(),
            matrix.ravel().tolist(),
        ):
            try:
                return constructor(qubits, representation)
            except (TypeError, ValueError) as error:
                last_error = error

    raise TypeError("Unable to construct a unitary gate with pyqpanda3.") from last_error
