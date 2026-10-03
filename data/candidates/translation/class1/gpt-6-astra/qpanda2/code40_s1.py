# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
import numpy as np
import pyqpanda as pq


def init_random_3qubit(desired_vector):
    vector = np.asarray(desired_vector, dtype=complex)
    if vector.shape != (8,):
        raise ValueError("desired_vector must contain exactly eight amplitudes.")
    norm = np.linalg.norm(vector)
    if not np.isfinite(norm) or not np.isclose(norm, 1.0, rtol=1e-10, atol=1e-10):
        raise ValueError("desired_vector must be normalized.")

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(3)
        cbits = machine.cAlloc_many(3)
        program = pq.QProg()

        for depth in range(3):
            block_size = 1 << (3 - depth)
            controls = [qubits[2 - j] for j in range(depth)]
            for prefix in range(1 << depth):
                start = prefix * block_size
                middle = start + block_size // 2
                end = start + block_size
                left = np.linalg.norm(vector[start:middle])
                right = np.linalg.norm(vector[middle:end])
                angle = float(2.0 * np.arctan2(right, left))

                zero_controls = [
                    controls[j]
                    for j in range(depth)
                    if ((prefix >> (depth - 1 - j)) & 1) == 0
                ]
                for qubit in zero_controls:
                    program << pq.X(qubit)
                gate = pq.RY(qubits[2 - depth], angle)
                if controls:
                    gate = gate.control(controls)
                program << gate
                for qubit in reversed(zero_controls):
                    program << pq.X(qubit)

        for index, amplitude in enumerate(vector):
            if amplitude == 0:
                continue
            angle = float(np.angle(amplitude))
            if angle == 0:
                continue
            zero_qubits = [
                qubits[j] for j in range(3) if ((index >> j) & 1) == 0
            ]
            for qubit in zero_qubits:
                program << pq.X(qubit)
            program << pq.U1(qubits[0], angle).control([qubits[1], qubits[2]])
            for qubit in reversed(zero_qubits):
                program << pq.X(qubit)

        for qubit, cbit in zip(qubits, cbits):
            program << pq.Measure(qubit, cbit)

        counts = machine.run_with_configuration(program, cbits, 4096)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        machine.finalize()
