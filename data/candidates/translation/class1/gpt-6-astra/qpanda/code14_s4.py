# EVAL_META: task_id=14, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, measure


def bell_each_shot():
    bell = QProg()
    bell << H(0) << CNOT(0, 1)
    bell << measure(0, 0) << measure(1, 1)

    backend = CPUQVM()
    backend.run(bell, 10)
    counts = backend.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
