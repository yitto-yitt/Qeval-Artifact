# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler


def init_random_3qubit(desired_vector):
    qc = QuantumCircuit(3)
    state = np.asarray(desired_vector, dtype=complex)
    qc.prepare_state(state, qc.qubits)
    qc.measure_all()

    backend = AerSimulator()
    sampler = Sampler(backend=backend)
    job = sampler.run([qc], shots=100000)
    result = job.result()
    quasi_dist = result.quasi_dists[0]

    dist = {format(i, "03b"): 0.0 for i in range(8)}
    for bitstring, prob in quasi_dist.items():
        if isinstance(bitstring, int):
            key = format(bitstring, "03b")
        else:
            key = str(bitstring).replace(" ", "")
        dist[key] = float(prob)

    return dist
