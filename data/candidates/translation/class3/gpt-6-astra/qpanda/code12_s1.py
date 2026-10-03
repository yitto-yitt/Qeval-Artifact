# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, H, X, CNOT


def get_unitary():
    def simulate(program):
        simulator = CPUQVM()
        run_result = simulator.run(program, 1)
        result_accessor = getattr(simulator, "result", None)
        result = result_accessor() if callable(result_accessor) else result_accessor

        for source in (result, run_result, simulator):
            if source is None:
                continue
            for name in (
                "get_state_vector",
                "get_statevector",
                "get_qstate",
                "state_vector",
                "statevector",
            ):
                accessor = getattr(source, name, None)
                if accessor is None:
                    continue
                state = accessor() if callable(accessor) else accessor
                vector = np.asarray(state, dtype=complex).reshape(-1)
                if vector.size == 4:
                    return vector
        raise RuntimeError("The simulator did not expose a two-qubit state vector.")

    calibration = QProg()
    calibration << X(1) << X(1) << X(0)
    calibration_state = simulate(calibration)
    bit_zero_index = int(np.argmax(np.abs(calibration_state)))
    if bit_zero_index == 1:
        row_order = [0, 1, 2, 3]
    elif bit_zero_index == 2:
        row_order = [0, 2, 1, 3]
    else:
        raise RuntimeError("Unexpected simulator basis ordering.")

    unitary = np.empty((4, 4), dtype=complex)
    for basis in range(4):
        program = QProg()
        if basis & 1:
            program << X(0)
        if basis & 2:
            program << X(1)
        program << H(0) << CNOT(0, 1)
        unitary[:, basis] = simulate(program)[row_order]

    return unitary
