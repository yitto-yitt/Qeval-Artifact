# EVAL_META: task_id=40, framework=qiskit, class=1

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2

def init_random_3qubit(desired_vector):
    vector = np.asarray(desired_vector, dtype=complex).reshape(-1)
    norm = np.linalg.norm(vector)
    if norm != 0:
        vector = vector / norm

    qc = QuantumCircuit(3)
    qc.initialize(vector, qc.qubits)
    qc.measure_all()

    backend = AerSimulator()
    try:
        sampler = SamplerV2(mode=backend)
    except TypeError:
        sampler = SamplerV2(backend=backend)

    job = sampler.run([qc], shots=10000)
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())

    prob_dist = {format(i, '03b'): 0.0 for i in range(8)}
    for bitstring, count in counts.items():
        prob_dist[bitstring] = count / total

    return prob_dist
