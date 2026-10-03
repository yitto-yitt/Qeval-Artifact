# EVAL_META: task_id=15, framework=qpanda, class=1
from collections import Counter
from random import Random
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, X, Y, Z, measure


def noisy_bell():
    shots = 1000
    rng = Random()
    simulator = CPUQVM()
    trajectories = Counter()

    # Sample gate-error trajectories and readout errors. The noise strengths
    # approximate a Belem-class device; pyQPanda has no FakeBelemV2 backend.
    for _ in range(shots):
        h_error = rng.randrange(1, 4) if rng.random() < 0.0006 else 0
        cx_error = rng.randrange(1, 16) if rng.random() < 0.015 else 0
        readout_0 = rng.random() < 0.025
        readout_1 = rng.random() < 0.025
        trajectories[(h_error, cx_error, readout_0, readout_1)] += 1

    paulis = (None, X, Y, Z)
    counts = Counter()

    for (h_error, cx_error, readout_0, readout_1), repetitions in trajectories.items():
        program = QProg()
        program << H(0)
        if h_error:
            program << paulis[h_error](0)

        program << CNOT(0, 1)
        error_0, error_1 = divmod(cx_error, 4)
        if error_0:
            program << paulis[error_0](0)
        if error_1:
            program << paulis[error_1](1)

        if readout_0:
            program << X(0)
        if readout_1:
            program << X(1)

        program << measure(0, 0) << measure(1, 1)
        simulator.run(program, repetitions)
        batch_counts = simulator.result().get_counts()
        for bitstring, count in batch_counts.items():
            key = format(bitstring, "02b") if isinstance(bitstring, int) else str(bitstring).replace(" ", "").zfill(2)
            counts[key] += count

    total = sum(counts.values())
    return {key: count / total for key, count in counts.items()}
