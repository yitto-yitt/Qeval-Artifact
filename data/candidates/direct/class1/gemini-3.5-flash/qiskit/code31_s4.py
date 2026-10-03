# EVAL_META: task_id=31, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2

def sampler_qiskit():
    # Initialize AerSimulator with the specified seed
    backend = AerSimulator(seed_simulator=42)
    
    # Initialize Qiskit Runtime Sampler V2 with the Aer backend
    sampler = SamplerV2(backend=backend)
    
    # Create a Bell circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Run the circuit
    job = sampler.run([qc])
    result = job.result()
    
    # Extract counts from the result
    pub_result = result[0]
    creg_name = qc.cregs[0].name
    bit_array = getattr(pub_result.data, creg_name)
    counts = bit_array.get_counts()
    
    # Convert counts to a probability distribution
    total_shots = sum(counts.values())
    prob_dist = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return prob_dist
