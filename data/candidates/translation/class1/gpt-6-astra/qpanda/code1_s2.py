# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, measure

def run_bell_state_simulator():
    bell = QProg()
    bell << H(0) << CNOT(0, 1)
    bell << measure(0, 0) << measure(1, 1)

    simulator = CPUQVM()
    result = simulator.run(bell, 1000)
    if not hasattr(result, "get_counts"):
        result = simulator.result()

    counts = result.get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
