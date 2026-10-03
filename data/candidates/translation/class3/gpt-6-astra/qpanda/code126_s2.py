# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def calculate_phase_difference_fidelity():
    gate = pq.H(0)
    circuit = pq.QCircuit()
    circuit << gate
    program = pq.QProg()
    program << circuit

    matrix_accessors = []
    for obj in (gate, circuit, program):
        for name in ("get_matrix", "matrix", "gate_matrix", "get_unitary", "get_unitary_matrix"):
            accessor = getattr(obj, name, None)
            if accessor is not None:
                matrix_accessors.append((accessor, ()))

    for name in ("get_matrix", "get_unitary", "get_circuit_matrix", "get_unitary_matrix"):
        accessor = getattr(pq, name, None)
        if callable(accessor):
            for obj in (circuit, program, gate):
                matrix_accessors.append((accessor, (obj,)))

    for accessor, args in matrix_accessors:
        try:
            matrix = accessor(*args) if callable(accessor) else accessor
            op_a = np.asarray(matrix, dtype=np.complex128).reshape(2, 2)
            if not np.allclose(op_a.conj().T @ op_a, np.eye(2)):
                continue
        except (TypeError, ValueError, RuntimeError):
            continue

        op_b = np.exp(0.5j) * op_a
        return float(abs(np.trace(op_a.conj().T @ op_b)) ** 2 / 4.0)

    raise RuntimeError("Unable to obtain the Hadamard operator matrix from pyQPanda3.")
