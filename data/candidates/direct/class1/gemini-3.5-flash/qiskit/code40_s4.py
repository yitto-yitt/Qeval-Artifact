# EVAL_META: task_id=40, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2

def init_random_3qubit(desired_vector):
    # Initialize a 3-qubit quantum circuit
    qc = QuantumCircuit(3)
    qc.initialize(desired_vector, [0, 1, 2])
    qc.measure_all()
    
    # Use AerSimulator backend with Qiskit Runtime SamplerV2
    backend = AerSimulator()
    sampler = SamplerV2(backend=backend)
    
    # Run the circuit
    job = sampler.run([qc])
    result = job.result()
    
    # Get counts from the 'meas' register
    pub_result = result[0]
    counts = pub_result.data.meas.get_counts()
    
    # Calculate probability distribution
    total_shots = sum(counts.values())
    prob_dist = {bitstr: count / total_shots for bitstr, count in counts.items()}
    
    return prob_dist
