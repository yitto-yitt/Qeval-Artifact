# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def init_random_3qubit(desired_vector):
    vec = np.asarray(desired_vector, dtype=complex)
    vec = vec / np.linalg.norm(vec)

    qc = QuantumCircuit(3)
    qc.initialize(vec, [0, 1, 2])
    qc.measure_all()

    backend = AerSimulator()
    isa = qc.copy()
    from qiskit import transpile
    isa = transpile(qc, backend)

    sampler = SamplerV2(mode=backend)
    result = sampler.run([isa], shots=4096).result()
    counts = result[0].data.meas.get_counts()

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
