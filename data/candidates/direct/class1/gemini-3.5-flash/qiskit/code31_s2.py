# EVAL_META: task_id=31, framework=qiskit, class=1

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2

def sampler_qiskit():
    # Create a Bell circuit
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr)
    qc.h(qr[0])
    qc.cx(qr[0], qr[1])
    qc.measure(qr, cr)
    
    # Initialize AerSimulator with seed
    backend = AerSimulator()
    backend.set_options(seed_simulator=42)
    
    # Initialize SamplerV2 with the backend
    sampler = SamplerV2(backend=backend)
    
    # Run the circuit
    job = sampler.run([qc])
    result = job.result()
    
    # Extract counts and calculate probabilities
    pub_result = result[0]
    counts = pub_result.data.c.get_counts()
    
    total_shots = sum(counts.values())
    probabilities = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return probabilities
