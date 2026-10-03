# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X, CNOT, measure

def visualize_bell_states():
    qvm = CPUQVM()
    qvm.init_qvm()

    q_plus = qvm.qAlloc_many(2)
    c_plus = qvm.cAlloc_many(2)
    prog_plus = QProg()
    prog_plus << H(q_plus[0])
    prog_plus << CNOT(q_plus[0], q_plus[1])
    prog_plus << measure(q_plus[0], c_plus[0])
    prog_plus << measure(q_plus[1], c_plus[1])
    counts_plus = qvm.run_with_configuration(prog_plus, c_plus, 1000)

    q_minus = qvm.qAlloc_many(2)
    c_minus = qvm.cAlloc_many(2)
    prog_minus = QProg()
    prog_minus << X(q_minus[0])
    prog_minus << H(q_minus[0])
    prog_minus << CNOT(q_minus[0], q_minus[1])
    prog_minus << measure(q_minus[0], c_minus[0])
    prog_minus << measure(q_minus[1], c_minus[1])
    counts_minus = qvm.run_with_configuration(prog_minus, c_minus, 1000)

    def to_prob(counts):
        total = sum(counts.values())
        dist = {}
        for k, v in counts.items():
            if isinstance(k, int):
                key = format(k, '02b')
            else:
                key = str(k)
                if len(key) < 2:
                    key = key.zfill(2)
            dist[key] = v / total
        return dist

    return {
        "phi_plus": to_prob(counts_plus),
        "phi_minus": to_prob(counts_minus),
    }
