# EVAL_META: task_id=40, framework=qpanda, class=1
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, RY, RZ, CNOT, measure

def init_random_3qubit(desired_vector):
    state = np.asarray(desired_vector, dtype=complex)
    if state.shape != (8,):
        raise ValueError("desired_vector must contain exactly eight amplitudes.")
    norm_squared = float(np.vdot(state, state).real)
    if not np.isfinite(norm_squared) or not np.isclose(
        norm_squared, 1.0, rtol=1e-10, atol=1e-10
    ):
        raise ValueError("desired_vector must be normalized.")

    prog = QProg()
    probabilities = np.abs(state) ** 2

    for target in (2, 1, 0):
        controls = list(range(target + 1, 3))
        num_patterns = 1 << len(controls)
        block_size = 1 << target
        angles = []

        for pattern in range(num_patterns):
            start = pattern << (target + 1)
            weight_zero = probabilities[start:start + block_size].sum()
            weight_one = probabilities[
                start + block_size:start + 2 * block_size
            ].sum()
            angles.append(
                2.0 * np.arctan2(np.sqrt(weight_one), np.sqrt(weight_zero))
            )

        for mask in range(num_patterns):
            angle = sum(
                angles[pattern]
                * (-1.0 if (pattern & mask).bit_count() % 2 else 1.0)
                for pattern in range(num_patterns)
            ) / num_patterns
            selected_controls = [
                control
                for index, control in enumerate(controls)
                if mask & (1 << index)
            ]
            for control in selected_controls:
                prog << CNOT(control, target)
            prog << RY(target, float(angle))
            for control in reversed(selected_controls):
                prog << CNOT(control, target)

    phases = np.angle(state)
    for mask in range(1, 8):
        coefficient = sum(
            phases[index]
            * (-1.0 if (index & mask).bit_count() % 2 else 1.0)
            for index in range(8)
        ) / 8.0
        involved = [qubit for qubit in range(3) if mask & (1 << qubit)]
        target = involved[0]
        controls = involved[1:]
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
    return {
        str(key).replace(" ", "").zfill(3): value / total
        for key, value in counts.items()
    }
