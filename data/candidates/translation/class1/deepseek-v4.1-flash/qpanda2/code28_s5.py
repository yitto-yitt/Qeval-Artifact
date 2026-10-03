# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def visualize_bell_states():
    qvm = CPUQVM()
    qvm.init_qvm()

    q_plus = qvm.qAlloc_many(2)
    c_plus = qvm.cAlloc_many(2)
    phi_plus = QProg()
    phi_plus << H(q_plus[0]) << CNOT(q_plus[0], q_plus[1]) << Measure(q_plus[0], c_plus[0]) << Measure(q_plus[1], c_plus[1])
    phi_plus_counts = qvm.run_with_configuration(phi_plus, c_plus, 1000)

    q_minus = qvm.qAlloc_many(2)
    c_minus = qvm.cAlloc_many(2)
    phi_minus = QProg()
    phi_minus << X(q_minus[0]) << H(q_minus[0]) << CNOT(q_minus[0], q_minus[1]) << Measure(q_minus[0], c_minus[0]) << Measure(q_minus[1], c_minus[1])
    phi_minus_counts = qvm.run_with_configuration(phi_minus, c_minus, 1000)

    phi_plus_total = builtins.sum(phi_plus_counts.values())
    phi_minus_total = builtins.sum(phi_minus_counts.values())

    qvm.finalize()

    return {
        "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
    }
