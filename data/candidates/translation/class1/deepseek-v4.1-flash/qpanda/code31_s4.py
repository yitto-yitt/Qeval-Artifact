# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict

from pyqpanda3.core import QProg, H, CNOT, Measure, CPUQVM


def sampler_qiskit():
    prog = QProg()
    prog << H(0) << CNOT(0, 1) << Measure(0, 0) << Measure(1, 1)

    qvm = CPUQVM()
    qvm.set_random_seed(42)
    result = qvm.run(prog, 1024)

    counts = result.get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
