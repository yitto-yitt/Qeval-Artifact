# EVAL_META: task_id=40, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def init_random_3qubit(desired_vector):
    backend = AerSimulator()

    qc = QuantumCircuit(3)
    qc.initialize(desired_vector, [0, 1, 2])
    qc.measure_all()

    isa_qc = transpile(qc, backend)

    sampler = SamplerV2(mode=backend)
    job = sampler.run([isa_qc])
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
