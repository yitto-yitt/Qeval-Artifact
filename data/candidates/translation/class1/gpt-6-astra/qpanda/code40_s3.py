# EVAL_META: task_id=40, framework=qpanda, class=1
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, X, RY, RZ, measure


def init_random_3qubit(desired_vector):
    amplitudes = np.asarray(desired_vector, dtype=complex)
    if amplitudes.shape != (8,):
        raise ValueError("desired_vector must contain exactly eight amplitudes.")
    if not np.all(np.isfinite(amplitudes)):
        raise ValueError("State amplitudes must be finite.")
    if not np.isclose(np.linalg.norm(amplitudes), 1.0, rtol=1e-10, atol=1e-10):
        raise ValueError("desired_vector must be normalized.")

    phases = np.angle(amplitudes)
    prog = QProg()

    for depth in range(3):
        target = 2 - depth
        controls = list(range(2, target, -1))
        block_size = 1 << (3 - depth)
        half = block_size // 2

        for prefix in range(1 << depth):
            start = prefix * block_size
            middle = start + half
            end = start + block_size

            left_norm = np.linalg.norm(amplitudes[start:middle])
            right_norm = np.linalg.norm(amplitudes[middle:end])
            theta = float(2.0 * np.arctan2(right_norm, left_norm))
            phi = float(
                np.mean(phases[middle:end]) - np.mean(phases[start:middle])
            )

            zero_controls = [
                qubit
                for index, qubit in enumerate(controls)
                if ((prefix >> (depth - index - 1)) & 1) == 0
            ]

            for qubit in zero_controls:
                prog << X(qubit)

            rotation_y = RY(target, theta)
            rotation_z = RZ(target, phi)
            if controls:
                rotation_y = rotation_y.control(controls)
                rotation_z = rotation_z.control(controls)
            prog << rotation_y << rotation_z

            for qubit in reversed(zero_controls):
                prog << X(qubit)

    for qubit in range(3):
        prog << measure(qubit, qubit)

    simulator = CPUQVM()
    simulator.run(prog, 4096)
    counts = simulator.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
