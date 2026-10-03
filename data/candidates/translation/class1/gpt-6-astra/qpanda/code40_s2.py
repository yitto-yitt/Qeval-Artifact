# EVAL_META: task_id=40, framework=qpanda, class=1
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, RY, RZ, CNOT, measure


def init_random_3qubit(desired_vector):
    state = np.asarray(desired_vector, dtype=complex)
    if state.shape != (8,):
        raise ValueError("desired_vector must contain exactly eight amplitudes.")
    if not np.all(np.isfinite(state)):
        raise ValueError("Amplitudes must be finite.")
    if not np.isclose(np.linalg.norm(state), 1.0, rtol=1e-10, atol=1e-10):
        raise ValueError("The state vector must be normalized.")

    prog = QProg()

    def uniformly_controlled_ry(target, controls, angles):
        count = len(angles)
        gray_codes = [i ^ (i >> 1) for i in range(count)]
        for i, gray in enumerate(gray_codes):
            angle = sum(
                (-1 if bin(gray & j).count("1") % 2 else 1) * angles[j]
                for j in range(count)
            ) / count
            prog.__lshift__(RY(target, float(angle)))
            if controls:
                changed = gray ^ gray_codes[(i + 1) % count]
                control = controls[changed.bit_length() - 1]
                prog.__lshift__(CNOT(control, target))

    for target in (2, 1, 0):
        half = 1 << target
        angles = []
        for base in range(0, 8, 2 * half):
            lower = np.linalg.norm(state[base:base + half])
            upper = np.linalg.norm(state[base + half:base + 2 * half])
            angles.append(2.0 * np.arctan2(upper, lower))
        uniformly_controlled_ry(target, list(range(target + 1, 3)), angles)

    phases = np.angle(state)
    for mask in range(1, 8):
        coefficient = sum(
            (-1 if bin(mask & index).count("1") % 2 else 1) * phases[index]
            for index in range(8)
        ) / 8.0
        involved = [qubit for qubit in range(3) if mask & (1 << qubit)]
        target = involved[-1]
        controls = involved[:-1]
        for control in controls:
            prog << CNOT(control, target)
        prog << RZ(target, float(-2.0 * coefficient))
        for control in reversed(controls):
            prog << CNOT(control, target)

    for qubit in range(3):
        prog << measure(qubit, qubit)

    simulator = CPUQVM()
    simulator.run(prog, 4096)
    counts = simulator.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
