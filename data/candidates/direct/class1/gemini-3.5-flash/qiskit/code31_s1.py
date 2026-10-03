# EVAL_META: task_id=31, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2

def sampler_qiskit():
    # Create a Bell circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Initialize AerSimulator with seed
    backend = AerSimulator(seed_simulator=42)
    
    # Initialize SamplerV2 with the backend
    sampler = SamplerV2(backend=backend)
    
    # Run the circuit
    job = sampler.run([qc])
    result = job.result()
    
    # Extract the counts
    pub_result = result[0]
    creg_name = qc.cregs[0].name
    bit_array = getattr(pub_result.data, creg_name)
    counts = bit_array.get_counts()
    
    # Calculate probabilities
    total_shots = sum(counts.values())
    probabilities = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return probabilities
