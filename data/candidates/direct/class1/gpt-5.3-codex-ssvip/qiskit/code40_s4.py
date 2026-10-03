# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def init_random_3qubit(desired_vector):
    qc = QuantumCircuit(3, 3)
    qc.initialize(desired_vector, [0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])

    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    job = sampler.run([qc], shots=4096)
    result = job.result()[0]

    if hasattr(result, "data") and hasattr(result.data, "c"):
        dist = result.data.c.get_counts()
    elif hasattr(result, "quasi_dists"):
        qd = result.quasi_dists[0]
        dist = {format(k, "03b"): float(v) for k, v in qd.items()}
    else:
        raise RuntimeError("Unsupported sampler result format.")

    total = float(sum(dist.values()))
    if total == 0:
        return {k: 0.0 for k in dist}
    return {k: float(v) / total for k, v in dist.items()}
