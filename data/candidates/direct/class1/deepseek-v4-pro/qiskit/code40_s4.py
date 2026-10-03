# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler


def init_random_3qubit(desired_vector):
    vec = np.asarray(desired_vector, dtype=complex)
    qc = QuantumCircuit(3)
    qc.initialize(vec, [0, 1, 2])
    qc.measure_all()

    backend = AerSimulator()
    sampler = Sampler(backend=backend)
    job = sampler.run([qc], shots=10000)

    result = job.result()
    pub_result = result[0]
    counts = pub_result.data.meas.get_counts()

    total_shots = sum(counts.values())
    return {bits: count / total_shots for bits, count in counts.items()}
