# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def visualize_bell_states():
    shots = 1000
    init(QMachineType.CPU)

    q_plus = qAlloc_many(2)
    c_plus = cAlloc_many(2)
    prog_plus = QProg()
    prog_plus << H(q_plus[0])
    prog_plus << CNOT(q_plus[0], q_plus[1])
    prog_plus << Measure(q_plus[0], c_plus[0])
    prog_plus << Measure(q_plus[1], c_plus[1])
    counts_plus = run_with_configuration(prog_plus, c_plus, shots)
    total_plus = builtins.sum(counts_plus.values())
    phi_plus_dist = {key: value / total_plus for key, value in counts_plus.items()}

    q_minus = qAlloc_many(2)
    c_minus = cAlloc_many(2)
    prog_minus = QProg()
    prog_minus << X(q_minus[0])
    prog_minus << H(q_minus[0])
    prog_minus << CNOT(q_minus[0], q_minus[1])
    prog_minus << Measure(q_minus[0], c_minus[0])
    prog_minus << Measure(q_minus[1], c_minus[1])
    counts_minus = run_with_configuration(prog_minus, c_minus, shots)
    total_minus = builtins.sum(counts_minus.values())
    phi_minus_dist = {key: value / total_minus for key, value in counts_minus.items()}

    return {
        "phi_plus": phi_plus_dist,
        "phi_minus": phi_minus_dist,
    }
