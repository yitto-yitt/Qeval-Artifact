# EVAL_META: task_id=15, framework=qpanda, class=1
from collections import Counter
from random import Random
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, X, Y, Z, measure


def noisy_bell():
    shots = 1000
    rng = Random()

    # Use a local stochastic noise approximation: pyQPanda3 does not
    # provide Qiskit's FakeBelemV2 calibration or Runtime pass manager.
    single_qubit_error = 0.001
    two_qubit_error = 0.015
    readout_errors = (0.025, 0.025)

    branches = Counter()
    for _ in range(shots):
        h_error = rng.randrange(4) if rng.random() < single_qubit_error else 0
        cx_error = rng.randrange(16) if rng.random() < two_qubit_error else 0
        readout_0 = rng.random() < readout_errors[0]
        readout_1 = rng.random() < readout_errors[1]
        branches[(h_error, cx_error, readout_0, readout_1)] += 1

    qvm = CPUQVM()
    counts = Counter()
    paulis = (None, X, Y, Z)

    for (h_error, cx_error, readout_0, readout_1), branch_shots in branches.items():
        program = QProg()
        program << H(0)
        if h_error:
            program << paulis[h_error](0)

        program << CNOT(0, 1)
        for qubit, error in enumerate((cx_error & 3, cx_error >> 2)):
            if error:
                program << paulis[error](qubit)

        if readout_0:
            program << X(0)
        if readout_1:
            program << X(1)

        program << measure(0, 0) << measure(1, 1)
        qvm.run(program, branch_shots)
        counts.update(qvm.result().get_counts())

    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
