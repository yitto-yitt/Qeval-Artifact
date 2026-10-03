# EVAL_META: task_id=28, framework=qpanda, class=1
import pyqpanda3.core as qp

def visualize_bell_states():
    qvm = qp.CPUQVM()
    qvm.init_qvm()

    # phi_plus
    q_plus = qvm.qAlloc_many(2)
    c_plus = qvm.cAlloc_many(2)
    prog_plus = qp.QProg()
    prog_plus << qp.H(q_plus[0])
    prog_plus << qp.CNOT(q_plus[0], q_plus[1])
    prog_plus << qp.Measure(q_plus[0], c_plus[0])
    prog_plus << qp.Measure(q_plus[1], c_plus[1])
    counts_plus = qvm.run_with_configuration(prog_plus, c_plus, 1000)

    # phi_minus
    q_minus = qvm.qAlloc_many(2)
    c_minus = qvm.cAlloc_many(2)
    prog_minus = qp.QProg()
    prog_minus << qp.X(q_minus[0])
    prog_minus << qp.H(q_minus[0])
    prog_minus << qp.CNOT(q_minus[0], q_minus[1])
    prog_minus << qp.Measure(q_minus[0], c_minus[0])
    prog_minus << qp.Measure(q_minus[1], c_minus[1])
    counts_minus = qvm.run_with_configuration(prog_minus, c_minus, 1000)

    def to_prob(counts):
        total = sum(counts.values())
        return {format(int(k), '02b'): v / total for k, v in counts.items()}

    return {
        "phi_plus": to_prob(counts_plus),
        "phi_minus": to_prob(counts_minus),
    }
