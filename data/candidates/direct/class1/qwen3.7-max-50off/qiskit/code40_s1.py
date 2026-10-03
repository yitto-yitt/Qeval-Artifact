# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def init_random_3qubit(desired_vector):
    qc = QuantumCircuit(3)
    qc.initialize(desired_vector, [0, 1, 2])
    qc.measure_all()

    backend = AerSimulator()
    sampler = SamplerV2(backend)
    job = sampler.run([qc], shots=8192)
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total_shots = sum(counts.values())
    prob_dist = {k: v / total_shots for k, v in counts.items()}

    return prob_dist
