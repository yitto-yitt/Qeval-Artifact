# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def init_random_3qubit(desired_vector):
    vec = Statevector(desired_vector).data
    qc = QuantumCircuit(3, 3)
    qc.initialize(vec, [0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])

    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    job = sampler.run([qc], shots=4096)
    result = job.result()

    pub_res = result[0]
    counts = pub_res.data.c.get_counts()
    total = sum(counts.values()) if counts else 1
    return {k: v / total for k, v in counts.items()}
