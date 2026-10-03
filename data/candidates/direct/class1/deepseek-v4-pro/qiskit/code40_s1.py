# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler

def init_random_3qubit(desired_vector):
    qc = QuantumCircuit(3)
    qc.initialize(desired_vector, range(3))
    backend = AerSimulator()
    sampler = Sampler(backend=backend)
    job = sampler.run([qc])
    result = job.result()
    quasi_dist = result.quasi_dists[0]
    prob_dict = {format(i, '03b'): 0.0 for i in range(8)}
    for state, prob in quasi_dist.items():
        prob_dict[format(state, '03b')] = float(prob)
    return prob_dict
