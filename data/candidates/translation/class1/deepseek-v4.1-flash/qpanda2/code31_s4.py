# EVAL_META: task_id=31, framework=qpanda2, class=1
import builtins
from pyqpanda import QProg, CPUQVM, H, CNOT, measure

def sampler_qiskit():
    qvm = CPUQVM()
    qvm.init_qvm()
    qvm.set_random_seed(42)

    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    prog << measure(q[0], c[0]) << measure(q[1], c[1])

    shots = 1024
    counts = qvm.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
