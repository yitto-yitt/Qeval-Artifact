# EVAL_META: task_id=40, framework=qiskit, class=1
import math
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def init_random_3qubit(desired_vector):
    vector = np.asarray(desired_vector, dtype=complex).flatten()
    if vector.size != 8:
        raise ValueError("desired_vector must contain exactly 8 amplitudes.")

    norm = np.linalg.norm(vector)
    if norm == 0:
        raise ValueError("desired_vector must not be the zero vector.")
    vector = vector / norm

    qc = QuantumCircuit(3, 3)
    qc.initialize(vector.tolist(), [0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])

    backend = AerSimulator()
    tqc = transpile(qc, backend)

    shots = 4096
    sampler = Sampler(mode=backend)
    job = sampler.run([tqc], shots=shots)
    result = job.result()
    pub_result = result[0]

    counts = None
    data = getattr(pub_result, "data", None)
    if data is not None:
        for name in ("c", "meas", "cr", "classical"):
            reg = getattr(data, name, None)
            if reg is not None and hasattr(reg, "get_counts"):
                counts = reg.get_counts()
                break
        if counts is None:
            for value in getattr(data, "__dict__", {}).values():
                if hasattr(value, "get_counts"):
                    counts = value.get_counts()
                    break

    if counts is None:
        counts = backend.run(tqc, shots=shots).result().get_counts()

    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in sorted(counts.items())}
