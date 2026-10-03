# EVAL_META: task_id=15, framework=qpanda, class=1
from math import asin, sqrt
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, RY, measure


def noisy_bell():
    program = QProg()
    program << H(0) << CNOT(0, 1)

    # Model local stochastic errors through unmeasured environment qubits.
    for qubit, environment in ((0, 2), (1, 3)):
        program << RY(environment, 2.0 * asin(sqrt(0.02)))
        program << CNOT(environment, qubit)

    program << measure(0, 0) << measure(1, 1)

    simulator = CPUQVM()
    simulator.run(program, 1000)
    counts = simulator.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
