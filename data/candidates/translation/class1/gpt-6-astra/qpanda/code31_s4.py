# EVAL_META: task_id=31, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, measure


def sampler_qiskit():
    qvm = CPUQVM()
    for method_name in ("set_seed", "set_random_seed", "set_rng_seed"):
        method = getattr(qvm, method_name, None)
        if callable(method):
            method(42)
            break

    prog = QProg()
    prog << H(0) << CNOT(0, 1)
    prog << measure(0, 0) << measure(1, 1)

    qvm.run(prog, 4096)
    counts = qvm.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
