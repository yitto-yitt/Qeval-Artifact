# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
import math
import numpy as np
import pyqpanda as pq


def init_random_3qubit(desired_vector):
    amplitudes = np.asarray(desired_vector, dtype=complex)
    if amplitudes.shape != (8,):
        raise ValueError("desired_vector must contain exactly eight amplitudes.")
    norm = float(np.linalg.norm(amplitudes))
    if not np.isfinite(norm) or not math.isclose(norm, 1.0, abs_tol=1e-10):
        raise ValueError("desired_vector must be normalized.")

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(3)
        cbits = machine.cAlloc_many(3)
        program = pq.QProg()

        for target in (2, 1, 0):
            half = 1 << target
            for prefix in range(1 << (2 - target)):
                start = prefix * (2 * half)
                left = float(np.linalg.norm(amplitudes[start:start + half]))
                right = float(
                    np.linalg.norm(amplitudes[start + half:start + 2 * half])
                )
                angle = 2.0 * math.atan2(right, left)
                controls = [qubits[j] for j in range(target + 1, 3)]
                flipped = [
                    qubits[j]
                    for j in range(target + 1, 3)
                    if not ((start >> j) & 1)
                ]

                for qubit in flipped:
                    program << pq.X(qubit)
                gate = pq.RY(qubits[target], angle)
                if controls:
                    gate = gate.control(controls)
                program << gate
                for qubit in reversed(flipped):
                    program << pq.X(qubit)

        for index, amplitude in enumerate(amplitudes):
            if abs(amplitude) == 0:
                continue
            phase = float(np.angle(amplitude))
            if phase == 0.0:
                continue
            flipped = [
                qubits[j] for j in range(3) if not ((index >> j) & 1)
            ]
            for qubit in flipped:
                program << pq.X(qubit)
            program << pq.U1(qubits[0], phase).control([qubits[1], qubits[2]])
            for qubit in reversed(flipped):
                program << pq.X(qubit)

        for qubit, cbit in zip(qubits, cbits):
            program << pq.Measure(qubit, cbit)

        counts = machine.run_with_configuration(program, cbits, 4096)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        machine.finalize()
