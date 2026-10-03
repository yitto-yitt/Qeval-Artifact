# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2

def bell_each_shot():
    # Create a Phi+ Bell circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Initialize AerSimulator backend
    backend = AerSimulator()
    
    # Transpile the circuit with optimization level 1
    transpiled_qc = transpile(qc, backend=backend, optimization_level=1)
    
    # Run using Qiskit Runtime SamplerV2
    sampler = SamplerV2(backend=backend)
    job = sampler.run([transpiled_qc], shots=10)
    result = job.result()
    
    # Extract counts and calculate probability distribution
    pub_result = result[0]
    counts = pub_result.data.meas.get_counts()
    
    total_shots = sum(counts.values())
    prob_dist = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return prob_dist
