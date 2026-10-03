# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def init_random_3qubit(desired_vector):
    vec = np.asarray(desired_vector, dtype=complex)
    norm = np.linalg.norm(vec)
    if norm == 0:
        raise ValueError("desired_vector must be non-zero")
    vec = vec / norm

    qc = QuantumCircuit(3)
    qc.initialize(vec, [0, 1, 2])
    qc.measure_all()

    backend = AerSimulator()
    sampler = SamplerV2(mode=backend)
    job = sampler.run([qc], shots=4096)
    result = job.result()
    counts = result[0].data.meas.get_counts()

    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
