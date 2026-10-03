# EVAL_META: task_id=15, framework=qpanda, class=1
from math import asin, sqrt
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, RY, measure


def noisy_bell():
    program = QProg()
    program << H(0) << CNOT(0, 1)

    # Ancilla-based stochastic channels model gate and readout errors.
    # Backend-specific calibration is not portable to pyQPanda.
    error_channels = (
        (0, 0.005),
        (1, 0.005),
        (0, 0.02),
        (1, 0.03),
    )
    for ancilla, (target, probability) in enumerate(error_channels, start=2):
        program << RY(ancilla, 2.0 * asin(sqrt(probability)))
        program << CNOT(ancilla, target)

    program << measure(0, 0) << measure(1, 1)

    simulator = CPUQVM()
    execution = simulator.run(program, 1000)
    if not hasattr(execution, "get_counts"):
        execution = simulator.result()
    counts = execution.get_counts()

    normalized_counts = {}
    for key, count in counts.items():
        bitstring = format(key, "02b") if isinstance(key, int) else str(key)
        bitstring = bitstring.replace(" ", "").removeprefix("0b").zfill(2)
        normalized_counts[bitstring] = normalized_counts.get(bitstring, 0) + count

    total = sum(normalized_counts.values())
    return {key: count / total for key, count in normalized_counts.items()}
