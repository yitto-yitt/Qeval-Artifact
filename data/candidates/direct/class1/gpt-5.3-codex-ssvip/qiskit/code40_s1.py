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
    result = job.result()

    pub_res = result[0]
    if hasattr(pub_res.data, "c"):
        counts = pub_res.data.c.get_counts()
    elif hasattr(pub_res.data, "meas"):
        counts = pub_res.data.meas.get_counts()
    else:
        counts = {}
        for attr in dir(pub_res.data):
            if attr.startswith("_"):
                continue
            obj = getattr(pub_res.data, attr)
            if hasattr(obj, "get_counts"):
                counts = obj.get_counts()
                break

    total = sum(counts.values()) if counts else 0
    if total == 0:
        return {}
    return {k: v / total for k, v in counts.items()}
