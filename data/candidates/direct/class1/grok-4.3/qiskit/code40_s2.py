# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import Sampler
from qiskit_aer import AerSimulator

def init_random_3qubit(desired_vector):
    desired_vector = np.asarray(desired_vector, dtype=complex)
    qc = QuantumCircuit(3)
    qc.initialize(desired_vector, range(3))
    qc.measure_all()
    backend = AerSimulator()
    sampler = Sampler(backend=backend)
    job = sampler.run([qc], shots=4096)
    result = job.result()
    probs = result.quasi_dists[0].binary_probabilities()
    return probs
