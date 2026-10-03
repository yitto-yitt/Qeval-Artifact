# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import init_qvm, destroy_qvm, qalloc, cbit_alloc, QProg, H, CNOT, X, measure, run_with_configuration

def visualize_bell_states():
    init_qvm()
    try:
        q_plus = qalloc(2)
        c_plus = cbit_alloc(2)
        prog_plus = QProg()
        prog_plus << H(q_plus[0]) << CNOT(q_plus[0], q_plus[1]) << measure(q_plus[0], c_plus[0]) << measure(q_plus[1], c_plus[1])
        counts_plus = run_with_configuration(prog_plus, c_plus, 1000)

        q_minus = qalloc(2)
        c_minus = cbit_alloc(2)
        prog_minus = QProg()
        prog_minus << X(q_minus[0]) << H(q_minus[0]) << CNOT(q_minus[0], q_minus[1]) << measure(q_minus[0], c_minus[0]) << measure(q_minus[1], c_minus[1])
        counts_minus = run_with_configuration(prog_minus, c_minus, 1000)

        total_plus = sum(counts_plus.values())
        total_minus = sum(counts_minus.values())
        return {
            "phi_plus": {key: value / total_plus for key, value in counts_plus.items()},
            "phi_minus": {key: value / total_minus for key, value in counts_minus.items()},
        }
    finally:
        destroy_qvm()
