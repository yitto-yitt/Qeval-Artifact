# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def get_unitary():
    prog = pq.QProg()
    prog << pq.H(0) << pq.CNOT(0, 1)

    for owner, args in ((prog, ()), (pq, (prog,))):
        for name in ("get_unitary", "get_matrix", "matrix", "unitary"):
            method = getattr(owner, name, None)
            if method is None:
                continue
            try:
                value = method(*args) if callable(method) else method
                matrix = np.asarray(value, dtype=complex)
                if matrix.size == 16:
                    return matrix.reshape(4, 4)
            except (TypeError, ValueError, RuntimeError):
                continue

    columns = []
    for basis in range(4):
        preparation = pq.QProg()
        for qubit in range(2):
            if basis & (1 << qubit):
                preparation << pq.X(qubit)
        preparation << pq.H(0) << pq.CNOT(0, 1)

        simulator = pq.CPUQVM()
        simulator.run(preparation, 1)
        result = simulator.result()
        state = None

        for owner in (result, simulator):
            for name in (
                "get_state_vector",
                "get_statevector",
                "get_qstate",
                "get_state",
                "state_vector",
                "statevector",
            ):
                accessor = getattr(owner, name, None)
                if accessor is None:
                    continue
                try:
                    value = accessor() if callable(accessor) else accessor
                    candidate = np.asarray(value, dtype=complex).reshape(-1)
                    if candidate.size == 4:
                        state = candidate
                        break
                except (TypeError, ValueError, RuntimeError):
                    continue
            if state is not None:
                break

        if state is None:
            raise RuntimeError("The simulator did not expose its state vector.")
        columns.append(state)

    return np.column_stack(columns)
