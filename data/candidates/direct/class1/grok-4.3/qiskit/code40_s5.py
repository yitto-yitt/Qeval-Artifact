# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_aer import AerSimulator
import numpy as np

def init_random_3qubit(desired_vector):
    qc = QuantumCircuit(3)
    qc.initialize(desired_vector, range(3))
    qc.measure_all()
    backend = AerSimulator()
    sampler = Sampler(backend=backend)
    pub = (qc,)
    job = sampler.run([pub], shots=4096)
    result = job.result()
    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
