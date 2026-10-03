# EVAL_META: task_id=31, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, measure


def sampler_qiskit():
    simulator = CPUQVM()
    for name in ("set_seed", "set_random_seed", "set_simulator_seed"):
        setter = getattr(simulator, name, None)
        if callable(setter):
            setter(42)
            break

    program = QProg()
    program << H(0) << CNOT(0, 1)
    program << measure(0, 0) << measure(1, 1)

    simulator.run(program, 4096)
    counts = simulator.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
