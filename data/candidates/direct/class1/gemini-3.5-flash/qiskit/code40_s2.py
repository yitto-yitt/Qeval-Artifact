# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2

def init_random_3qubit(desired_vector):
    # Initialize a 3-qubit quantum circuit
    qc = QuantumCircuit(3)
    qc.initialize(desired_vector, [0, 1, 2])
    qc.measure_all()
    
    # Use AerSimulator as the backend for the Sampler
    backend = AerSimulator()
    sampler = SamplerV2(backend=backend)
    
    # Run the sampler job
    job = sampler.run([qc])
    result = job.result()
    
    # Extract counts and calculate probability distribution
    pub_result = result[0]
    creg_name = qc.cregs[0].name
    counts = getattr(pub_result.data, creg_name).get_counts()
    
    total_shots = sum(counts.values())
    probabilities = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return probabilities
