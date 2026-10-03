# EVAL_META: task_id=31, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler, Session

def sampler_qiskit():
    # Create Bell circuit
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    # Aer simulator with fixed seed
    backend = AerSimulator(seed_simulator=42)

    # Use Qiskit Runtime Sampler primitive
    with Session(backend=backend) as session:
        sampler = Sampler(session=session)
        job = sampler.run([qc])
        result = job.result()

    # Extract quasi-probability distribution
    quasi_dist = result.quasi_dists[0]

    # Convert integer keys to bitstring keys
    prob_dict = {format(k, '0{}b'.format(qc.num_clbits)): v for k, v in quasi_dist.items()}
    return prob_dict
