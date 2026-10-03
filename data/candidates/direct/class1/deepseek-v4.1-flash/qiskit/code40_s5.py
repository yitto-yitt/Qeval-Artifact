# EVAL_META: task_id=40, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
import numpy as np

def init_random_3qubit(desired_vector):
    # Create a 3-qubit quantum circuit
    qc = QuantumCircuit(3)
    # Initialize the qubits to the desired state
    qc.initialize(desired_vector, [0, 1, 2])
    # Measure all qubits (adds a classical register named 'meas')
    qc.measure_all()

    # Use Aer simulator as the backend
    backend = AerSimulator()
    # Create the Qiskit Runtime Sampler
    sampler = Sampler(backend=backend)
    # Run the sampler with a fixed number of shots
    job = sampler.run([qc], shots=1024)
    result = job.result()

    # Extract measurement counts
    counts = result[0].data.meas.get_counts()
    total_shots = sum(counts.values())
    # Convert counts to a probability distribution
    prob_dist = {bitstring: count / total_shots for bitstring, count in counts.items()}
    return prob_dist
