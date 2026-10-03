# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import QProg, H, CNOT, measure, CPUQVM

def noisy_bell():
    prog = QProg()
    prog << H(0) << CNOT(0, 1)
    prog << measure(0, 0) << measure(1, 1)
    machine = CPUQVM()
    machine.run(prog, 1000)
    counts = machine.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
