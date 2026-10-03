# EVAL_META: task_id=28, framework=qpanda2, class=1
from pyqpanda import *


def visualize_bell_states():
    shots = 1000

    init(QMachineType.CPU)

    # phi_plus
    q_plus = qAlloc_many(2)
    c_plus = cAlloc_many(2)
    prog_plus = QProg()
    prog_plus << H(q_plus[0]) << CNOT(q_plus[0], q_plus[1]) << measure_all(q_plus, c_plus)
    counts_plus = run_with_configuration(prog_plus, c_plus, shots)

    # phi_minus
    q_minus = qAlloc_many(2)
    c_minus = cAlloc_many(2)
    prog_minus = QProg()
    prog_minus << X(q_minus[0]) << H(q_minus[0]) << CNOT(q_minus[0], q_minus[1]) << measure_all(q_minus, c_minus)
    counts_minus = run_with_configuration(prog_minus, c_minus, shots)

    finalize()

    return {
        "phi_plus": {key: value / shots for key, value in counts_plus.items()},
        "phi_minus": {key: value / shots for key, value in counts_minus.items()},
    }
