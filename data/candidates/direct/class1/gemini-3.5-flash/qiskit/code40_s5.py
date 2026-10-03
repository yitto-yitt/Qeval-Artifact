# EVAL_META: task_id=40, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2

def init_random_3qubit(desired_vector):
    # Create a 3-qubit quantum circuit
    qc = QuantumCircuit(3)
    
    # Initialize the circuit with the desired state vector
    qc.initialize(desired_vector, [0, 1, 2])
    
    # Measure all qubits
    qc.measure_all()
    
    # Initialize the Aer simulator backend
    backend = AerSimulator()
    
    # Initialize the Qiskit Runtime Sampler with the Aer backend
    sampler = SamplerV2(backend=backend)
    
    # Run the circuit using the sampler
    job = sampler.run([qc])
    result = job.result()
    
    # Retrieve the counts from the classical register (default name is 'meas')
    pub_result = result[0]
    creg_name = qc.cregs[0].name
    counts = getattr(pub_result.data, creg_name).get_counts()
    
    # Convert counts to a probability distribution
    total_shots = sum(counts.values())
    prob_dist = {bitstr: count / total_shots for bitstr, count in counts.items()}
    
    return prob_dist
