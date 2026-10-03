# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
import pyqpanda as pq


def visualize_bell_states():
    shots = 1000

    qvm = pq.CPUQVM()
    qvm.init_qvm()

    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)

    prog_plus = pq.QProg()
    prog_plus << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    counts_plus = qvm.run_with_configuration(prog_plus, c, shots)

    prog_minus = pq.QProg()
    prog_minus << pq.X(q[0]) << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    counts_minus = qvm.run_with_configuration(prog_minus, c, shots)

    total_plus = builtins.sum(counts_plus.values())
    total_minus = builtins.sum(counts_minus.values())

    result = {
        "phi_plus": {k: v / total_plus for k, v in counts_plus.items()},
        "phi_minus": {k: v / total_minus for k, v in counts_minus.items()},
    }

    qvm.finalize()
    return result
