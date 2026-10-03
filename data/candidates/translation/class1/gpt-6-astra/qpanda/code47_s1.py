# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, measure

def random_coin_flip(samples):
    circuit = QProg()
    circuit << H(0) << measure(0, 0)
    simulator = CPUQVM()
    simulator.run(circuit, samples)
    counts = simulator.result().get_counts()
    total = sum(counts.values())
    return {
        'Heads': counts.get('0', 0) / total,
        'Tails': counts.get('1', 0) / total,
    }
