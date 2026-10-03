# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def init_random_3qubit(desired_vector):
    backend = AerSimulator()

    qc = QuantumCircuit(3)
    qc.initialize(desired_vector, [0, 1, 2])
    qc.measure_all()

    sampler = Sampler(mode=backend)
    job = sampler.run([qc])
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    probs = {bitstring: count / total for bitstring, count in counts.items()}

    return probs
