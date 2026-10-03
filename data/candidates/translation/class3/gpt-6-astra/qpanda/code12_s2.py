# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def get_unitary():
    circuit = pq.QCircuit()
    circuit << pq.H(0) << pq.CNOT(0, 1)
    program = pq.QProg()
    program << circuit

    for owner, arguments in (
        (pq, (circuit,)),
        (pq, (program,)),
        (circuit, ()),
        (program, ()),
    ):
        for name in ("get_matrix", "get_unitary", "to_matrix", "matrix",
                     "circuit_to_matrix"):
            getter = getattr(owner, name, None)
            if getter is None:
                continue
            try:
                value = getter(*arguments) if callable(getter) else getter
                matrix = np.asarray(value, dtype=complex)
                if matrix.size == 16:
                    return matrix.reshape(4, 4)
            except (TypeError, ValueError, RuntimeError):
                continue

    columns = []
    for basis in range(4):
        simulator = pq.CPUQVM()
        preparation = pq.QProg()
        for qubit in range(2):
            if basis & (1 << qubit):
                preparation << pq.X(qubit)
        preparation << pq.H(0) << pq.CNOT(0, 1)

        try:
            result = simulator.run(preparation)
        except TypeError:
            result = simulator.run(preparation, 1)

        state = None
        owners = [simulator, result]
        result_getter = getattr(simulator, "result", None)
        if callable(result_getter):
            owners.append(result_getter())

        for owner in owners:
            if owner is None:
                continue
            for name in ("get_state_vector", "get_statevector", "get_qstate",
                         "state_vector", "statevector"):
                getter = getattr(owner, name, None)
                if getter is None:
                    continue
                try:
                    value = getter() if callable(getter) else getter
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
