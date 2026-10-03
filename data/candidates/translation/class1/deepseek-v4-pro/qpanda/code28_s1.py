# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, X, Measure

def visualize_bell_states():
    qvm = CPUQVM()
    qvm.init_qvm()

    # phi_plus circuit: |Φ+⟩ = (|00⟩ + |11⟩)/√2
    q_plus = qvm.qAlloc_many(2)
    c_plus = qvm.cAlloc_many(2)
    prog_plus = QProg()
    prog_plus << H(q_plus[0]) \
              << CNOT(q_plus[0], q_plus[1]) \
              << Measure(q_plus[0], c_plus[0]) \
              << Measure(q_plus[1], c_plus[1])

    # phi_minus circuit: |Φ-⟩ = (|00⟩ - |11⟩)/√2
    q_minus = qvm.qAlloc_many(2)
    c_minus = qvm.cAlloc_many(2)
    prog_minus = QProg()
    prog_minus << X(q_minus[0]) \
               << H(q_minus[0]) \
               << CNOT(q_minus[0], q_minus[1]) \
               << Measure(q_minus[0], c_minus[0]) \
               << Measure(q_minus[1], c_minus[1])

    # Run with 1000 shots
    counts_plus = qvm.run_with_configuration(prog_plus, c_plus, 1000)
    counts_minus = qvm.run_with_configuration(prog_minus, c_minus, 1000)

    # Normalize to probabilities
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    prob_plus = {k: v / total_plus for k, v in counts_plus.items()}
    prob_minus = {k: v / total_minus for k, v in counts_minus.items()}

    qvm.finalize()

    return {
        "phi_plus": prob_plus,
        "phi_minus": prob_minus
    }
