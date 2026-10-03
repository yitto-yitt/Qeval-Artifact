# EVAL_META: task_id=40, framework=qpanda, class=1
import numpy as np
import pyqpanda3.core as pq


def init_random_3qubit(desired_vector):
    vector = np.asarray(desired_vector, dtype=complex)
    if vector.shape != (8,):
        raise ValueError("desired_vector must contain exactly eight amplitudes.")
    if not np.all(np.isfinite(vector)):
        raise ValueError("State amplitudes must be finite.")
    if not np.isclose(np.linalg.norm(vector), 1.0, rtol=1e-10, atol=1e-10):
        raise ValueError("The state vector must be normalized.")

    prog = pq.QProg()

    for target in (2, 1, 0):
        controls = list(range(target + 1, 3))
        branches = 1 << len(controls)
        angles = []
        width = 1 << target

        for pattern in range(branches):
            base = sum(
                ((pattern >> j) & 1) << control
                for j, control in enumerate(controls)
            )
            norm_zero = np.linalg.norm(vector[base:base + width])
            norm_one = np.linalg.norm(vector[base + width:base + 2 * width])
            angles.append(2.0 * np.arctan2(norm_one, norm_zero))

        for mask in range(branches):
            angle = sum(
                theta * (-1 if bin(pattern & mask).count("1") % 2 else 1)
                for pattern, theta in enumerate(angles)
            ) / branches
            selected = [
                control
                for j, control in enumerate(controls)
                if (mask >> j) & 1
            ]
            for control in selected:
                prog << pq.CNOT(control, target)
            prog << pq.RY(target, float(angle))
            for control in reversed(selected):
                prog << pq.CNOT(control, target)

    phases = np.angle(vector)
    for mask in range(1, 8):
        coefficient = sum(
            phase * (-1 if bin(index & mask).count("1") % 2 else 1)
            for index, phase in enumerate(phases)
        ) / 8.0
        selected = [qubit for qubit in range(3) if (mask >> qubit) & 1]
        target = selected[-1]
        controls = selected[:-1]
        for control in controls:
            prog << pq.CNOT(control, target)
        prog << pq.RZ(target, float(-2.0 * coefficient))
        for control in reversed(controls):
            prog << pq.CNOT(control, target)

    measure = getattr(pq, "measure", None)
    if measure is None:
        measure = pq.Measure
    for qubit in range(3):
        prog << measure(qubit, qubit)

    simulator = pq.CPUQVM()
    simulator.run(prog, 4096)
    counts = simulator.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
