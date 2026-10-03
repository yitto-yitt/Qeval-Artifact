# EVAL_META: task_id=40, framework=qpanda2, class=1
import numpy as np
import pyqpanda as pq

def init_random_3qubit(desired_vector):
    state = np.asarray(desired_vector, dtype=complex)
    if state.shape != (8,) or not np.all(np.isfinite(state)):
        raise ValueError("desired_vector must contain eight finite complex amplitudes.")
    if not np.isclose(np.linalg.norm(state), 1.0, rtol=0.0, atol=1e-10):
        raise ValueError("desired_vector must be normalized.")

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(3)
        cbits = machine.cAlloc_many(3)
        program = pq.QProg()

        for depth in range(3):
            target = qubits[2 - depth]
            controls = [qubits[2 - j] for j in range(depth)]
            block_size = 1 << (3 - depth)
            half = block_size // 2

            for prefix in range(1 << depth):
                start = prefix * block_size
                left = float(np.linalg.norm(state[start:start + half]))
                right = float(np.linalg.norm(state[start + half:start + block_size]))
                angle = 2.0 * np.arctan2(right, left)

                flipped = [
                    controls[j]
                    for j in range(depth)
                    if ((prefix >> (depth - 1 - j)) & 1) == 0
                ]
                for qubit in flipped:
                    program << pq.X(qubit)

                gate = pq.RY(target, float(angle))
                if controls:
                    gate = gate.control(controls)
                program << gate

                for qubit in reversed(flipped):
                    program << pq.X(qubit)

        for index, amplitude in enumerate(state):
            phase = float(np.angle(amplitude))
            if phase == 0.0:
                continue

            flipped = [
                qubits[j] for j in range(3) if ((index >> j) & 1) == 0
            ]
            for qubit in flipped:
                program << pq.X(qubit)

            program << pq.U1(qubits[0], phase).control([qubits[1], qubits[2]])

            for qubit in reversed(flipped):
                program << pq.X(qubit)

        program << pq.measure_all(qubits, cbits)
        shots = 4096
        counts = machine.run_with_configuration(program, cbits, shots)
        return {key: value / shots for key, value in counts.items()}
    finally:
        machine.finalize()
