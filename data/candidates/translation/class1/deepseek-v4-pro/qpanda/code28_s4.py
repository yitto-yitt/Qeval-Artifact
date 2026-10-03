# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import init_qvm, qAlloc_many, cAlloc_many, QProg, H, X, CNOT, Measure, run_with_configuration

def visualize_bell_states():
    init_qvm()

    q_plus = qAlloc_many(2)
    c_plus = cAlloc_many(2)
    prog_plus = QProg()
    prog_plus << H(q_plus[0]) << CNOT(q_plus[0], q_plus[1]) << Measure(q_plus[0], c_plus[0]) << Measure(q_plus[1], c_plus[1])
    phi_plus_counts = run_with_configuration(prog_plus, c_plus, 1000)

    q_minus = qAlloc_many(2)
    c_minus = cAlloc_many(2)
    prog_minus = QProg()
    prog_minus << X(q_minus[0]) << H(q_minus[0]) << CNOT(q_minus[0], q_minus[1]) << Measure(q_minus[0], c_minus[0]) << Measure(q_minus[1], c_minus[1])
    phi_minus_counts = run_with_configuration(prog_minus, c_minus, 1000)

    phi_plus_total = sum(phi_plus_counts.values())
    phi_minus_total = sum(phi_minus_counts.values())

    return {
        "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
    }
