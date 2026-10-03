# EVAL_META: task_id=1, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2

def run_bell_state_simulator():
    # Define a phi plus Bell state (|00> + |11>) / sqrt(2)
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Initialize Aer simulator backend
    backend = AerSimulator()
    
    # Transpile the circuit with a preset pass manager at optimization level 1
    transpiled_qc = transpile(qc, backend=backend, optimization_level=1)
    
    # Run with Qiskit Runtime Sampler on the Aer simulator backend
    sampler = SamplerV2(backend=backend)
    job = sampler.run([transpiled_qc])
    result = job.result()
    
    # Extract the measurement results
    pub_result = result[0]
    creg_name = transpiled_qc.cregs[0].name
    bit_array = getattr(pub_result.data, creg_name)
    counts = bit_array.get_counts()
    
    # Calculate the probability distribution
    total_shots = sum(counts.values())
    prob_dist = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return prob_dist
