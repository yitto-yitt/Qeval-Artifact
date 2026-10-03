# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import QProg, H, CNOT, X, Measure, CPUQVM

def visualize_bell_states():
    def run_state(prep):
        qvm = CPUQVM()
        qvm.init_qvm()
        q = qvm.qAlloc_many(2)
        c = qvm.cAlloc_many(2)
        prog = QProg()
        prep(prog, q)
        prog << Measure(q[0], c[0]) << Measure(q[1], c[1])
        counts = qvm.run_with_configuration(prog, c, 1000)
        qvm.finalize()
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}

    def phi_plus(prog, q):
        prog << H(q[0]) << CNOT(q[0], q[1])

    def phi_minus(prog, q):
        prog << X(q[0]) << H(q[0]) << CNOT(q[0], q[1])

    return {
        "phi_plus": run_state(phi_plus),
        "phi_minus": run_state(phi_minus),
    }
