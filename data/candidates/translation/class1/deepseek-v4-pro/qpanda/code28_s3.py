# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import *

def visualize_bell_states():
    qvm = CPUQVM()
    qvm.init()

    # Phi plus: (|00> + |11>) / sqrt(2)
    q_plus = qvm.qAlloc_many(2)
    c_plus = qvm.cAlloc_many(2)
    prog_plus = QProg()
    prog_plus << H(q_plus[0]) << CNOT(q_plus[0], q_plus[1]) \
              << Measure(q_plus[0], c_plus[0]) << Measure(q_plus[1], c_plus[1])
    counts_plus = qvm.run_with_configuration(prog_plus, c_plus, 1000)

    # Phi minus: (|00> - |11>) / sqrt(2)
    q_minus = qvm.qAlloc_many(2)
    c_minus = qvm.cAlloc_many(2)
    prog_minus = QProg()
    prog_minus << X(q_minus[0]) << H(q_minus[0]) << CNOT(q_minus[0], q_minus[1]) \
               << Measure(q_minus[0], c_minus[0]) << Measure(q_minus[1], c_minus[1])
    counts_minus = qvm.run_with_configuration(prog_minus, c_minus, 1000)

    qvm.finalize()

    plus_total = sum(counts_plus.values())
    minus_total = sum(counts_minus.values())

    return {
        "phi_plus": {key: value / plus_total for key, value in counts_plus.items()},
        "phi_minus": {key: value / minus_total for key, value in counts_minus.items()},
    }
