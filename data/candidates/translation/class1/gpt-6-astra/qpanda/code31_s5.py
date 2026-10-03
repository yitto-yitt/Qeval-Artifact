# EVAL_META: task_id=31, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, measure

def sampler_qiskit():
    prog = QProg()
    prog << H(0) << CNOT(0, 1)
    prog << measure(0, 0) << measure(1, 1)

    simulator = CPUQVM()
    for method_name in ("set_random_seed", "set_seed"):
        seed_method = getattr(simulator, method_name, None)
        if callable(seed_method):
            seed_method(42)
            break

    simulator.run(prog, 4096)
    counts = simulator.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
