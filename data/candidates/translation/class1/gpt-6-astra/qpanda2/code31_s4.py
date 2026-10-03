# EVAL_META: task_id=31, framework=qpanda2, class=1
import numpy as np
import pyqpanda as pq


def sampler_qiskit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(2)
        program = pq.QProg()
        program << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])

        probabilities = machine.prob_run_dict(program, qubits, -1)
        bitstrings = sorted(probabilities)
        weights = np.array(
            [probabilities[key] for key in bitstrings], dtype=float
        )
        weights /= weights.sum()

        shots = 4096
        counts = np.random.default_rng(42).multinomial(shots, weights)
        return {
            key: int(count) / shots
            for key, count in zip(bitstrings, counts)
            if count
        }
    finally:
        machine.finalize()
