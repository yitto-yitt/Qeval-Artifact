# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

def init_random_3qubit(desired_vector):
    qc = QuantumCircuit(3)
    qc.initialize(desired_vector, [0, 1, 2])
    qc.measure_all()
    backend = AerSimulator()
    sampler = Sampler(backend=backend)
    job = sampler.run([qc], shots=1024)
    result = job.result()
    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
