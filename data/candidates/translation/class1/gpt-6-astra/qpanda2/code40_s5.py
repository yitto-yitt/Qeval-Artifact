# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
import numpy as np
import pyqpanda as pq


def init_random_3qubit(desired_vector):
    amplitudes = np.asarray(desired_vector, dtype=complex)
    if amplitudes.shape != (8,):
        raise ValueError("desired_vector must contain exactly eight amplitudes.")
    if not np.all(np.isfinite(amplitudes)):
        raise ValueError("Amplitudes must be finite.")
    if not np.isclose(np.linalg.norm(amplitudes), 1.0):
        raise ValueError("desired_vector must be normalized.")

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(3)
        cbits = machine.cAlloc_many(3)
        program = pq.QProg()

        for target in (2, 1, 0):
            control_indices = list(range(target + 1, 3))
            controls = [qubits[index] for index in control_indices]
            block_size = 1 << (target + 1)
            half_size = 1 << target

            for prefix in range(1 << (2 - target)):
                start = prefix * block_size
                lower_norm = np.linalg.norm(
                    amplitudes[start:start + half_size]
                )
                upper_norm = np.linalg.norm(
                    amplitudes[start + half_size:start + block_size]
                )
                angle = float(2.0 * np.arctan2(upper_norm, lower_norm))
                flipped = [
                    index for index in control_indices
                    if ((prefix >> (index - target - 1)) & 1) == 0
                ]

                for index in flipped:
                    program << pq.X(qubits[index])

                rotation = pq.RY(qubits[target], angle)
                if controls:
                    rotation = rotation.control(controls)
                program << rotation

                for index in reversed(flipped):
                    program << pq.X(qubits[index])

        for basis_index, amplitude in enumerate(amplitudes):
            if amplitude == 0:
                continue
            phase = float(np.angle(amplitude))
            if phase == 0:
                continue

            flipped = [
                index for index in range(3)
                if ((basis_index >> index) & 1) == 0
            ]
            for index in flipped:
                program << pq.X(qubits[index])

            program << pq.U1(qubits[0], phase).control(
                [qubits[1], qubits[2]]
            )

            for index in reversed(flipped):
                program << pq.X(qubits[index])

        for qubit, cbit in zip(qubits, cbits):
            program << pq.Measure(qubit, cbit)

        counts = machine.run_with_configuration(program, cbits, 4096)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        machine.finalize()
