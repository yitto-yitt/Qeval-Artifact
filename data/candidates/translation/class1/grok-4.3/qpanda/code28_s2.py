# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X, CNOT, Measure

def visualize_bell_states():
    qvm_plus = CPUQVM()
    qvm_plus.init_qvm()
    q_plus = qvm_plus.qAlloc_many(2)
    c_plus = qvm_plus.cAlloc_many(2)
    prog_plus = QProg()
    prog_plus << H(q_plus[0]) << CNOT(q_plus[0], q_plus[1]) << Measure(q_plus[0], c_plus[0]) << Measure(q_plus[1], c_plus[1])
    counts_plus = qvm_plus.run_with_configuration(prog_plus, c_plus, 1000)
    total_plus = sum(counts_plus.values())
    dist_plus = {k: v / total_plus for k, v in counts_plus.items()}
    qvm_plus.finalize()

    qvm_minus = CPUQVM()
    qvm_minus.init_qvm()
    q_minus = qvm_minus.qAlloc_many(2)
    c_minus = qvm_minus.cAlloc_many(2)
    prog_minus = QProg()
    prog_minus << X(q_minus[0]) << H(q_minus[0]) << CNOT(q_minus[0], q_minus[1]) << Measure(q_minus[0], c_minus[0]) << Measure(q_minus[1], c_minus[1])
    counts_minus = qvm_minus.run_with_configuration(prog_minus, c_minus, 1000)
    total_minus = sum(counts_minus.values())
    dist_minus = {k: v / total_minus for k, v in counts_minus.items()}
    qvm_minus.finalize()

    return {
        "phi_plus": dist_plus,
        "phi_minus": dist_minus,
    }
