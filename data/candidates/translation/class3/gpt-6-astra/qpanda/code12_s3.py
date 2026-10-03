# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def get_unitary():
    circuit = pq.QCircuit()
    circuit << pq.H(0) << pq.CNOT(0, 1)
    program = pq.QProg()
    program << circuit

    for name in ("get_unitary", "get_unitary_matrix", "get_matrix", "matrix"):
        for owner in (program, circuit, pq):
            method = getattr(owner, name, None)
            if not callable(method):
                continue
            arguments = ((program,), (circuit,)) if owner is pq else ((),)
            for args in arguments:
                try:
                    matrix = np.asarray(method(*args), dtype=np.complex128)
                    if matrix.size == 16:
                        return matrix.reshape(4, 4)
                except (TypeError, ValueError, RuntimeError):
                    continue

    raise RuntimeError("The installed pyqpanda3 API could not extract the circuit unitary.")
