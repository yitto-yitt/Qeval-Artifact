# EVAL_META: task_id=40, framework=qpanda, class=1
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, RY, RZ, X, measure


def init_random_3qubit(desired_vector):
    amplitudes = np.asarray(desired_vector, dtype=complex)
    if amplitudes.shape != (8,):
        raise ValueError("desired_vector must contain exactly eight amplitudes.")
    if not np.all(np.isfinite(amplitudes)):
        raise ValueError("State amplitudes must be finite.")
    if not np.isclose(np.linalg.norm(amplitudes), 1.0, rtol=1e-10, atol=1e-10):
        raise ValueError("The state vector must be normalized.")

    prog = QProg()
    phases = np.angle(amplitudes)

    for phase_stage in (False, True):
        for depth in range(3):
            target = 2 - depth
            controls = list(range(2, target, -1))
            width = 1 << (3 - depth)
            half = width // 2

            for prefix in range(1 << depth):
                start = prefix * width
                middle = start + half
                end = start + width

                if phase_stage:
                    angle = float(
                        np.mean(phases[middle:end]) - np.mean(phases[start:middle])
                    )
                    gate = RZ(target, angle)
                else:
                    left_norm = np.linalg.norm(amplitudes[start:middle])
                    right_norm = np.linalg.norm(amplitudes[middle:end])
                    angle = float(2.0 * np.arctan2(right_norm, left_norm))
                    gate = RY(target, angle)

                zero_controls = [
                    qubit
                    for position, qubit in enumerate(controls)
                    if not ((prefix >> (depth - position - 1)) & 1)
                ]

                for qubit in zero_controls:
                    prog << X(qubit)
                if controls:
                    gate = gate.control(controls)
                prog << gate
                for qubit in reversed(zero_controls):
                    prog << X(qubit)

    for qubit in range(3):
        prog << measure(qubit, qubit)

    qvm = CPUQVM()
    qvm.run(prog, 4096)
    counts = qvm.result().get_counts()
    total = sum(counts.values())

    probabilities = {}
    for key, count in counts.items():
        if isinstance(key, (int, np.integer)):
            bitstring = format(int(key), "03b")
        else:
            bitstring = str(key).replace(" ", "")
            if bitstring.startswith(("0x", "0X")):
                bitstring = format(int(bitstring, 16), "03b")
            else:
                bitstring = bitstring.removeprefix("0b").zfill(3)
        probabilities[bitstring] = probabilities.get(bitstring, 0.0) + count / total

    return probabilities
