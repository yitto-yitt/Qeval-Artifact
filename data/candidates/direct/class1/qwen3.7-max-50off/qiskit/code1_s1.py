# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

def run_bell_state_simulator():
    # Initialize backend
    backend = AerSimulator()
    
    # Define Phi+ Bell State
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Transpile with optimization level 1
    isa_circuit = transpile(qc, backend, optimization_level=1)
    
    # Run with Qiskit Runtime Sampler
    sampler = Sampler(backend=backend)
    job = sampler.run([isa_circuit])
    result = job.result()
    
    # Extract results
    # In SamplerV2, results are in PubResult objects. 
    # measure_all() creates a classical register named 'meas'.
    pub_result = result[0]
    bit_array = pub_result.data.meas
    
    # Get counts (keys are hex strings in Qiskit 1.x+/2.x BitArray)
    counts = bit_array.get_counts()
    total_shots = sum(counts.values())
    
    # Convert to probability distribution with binary bitstring keys
    probs = {}
    for k, v in counts.items():
        # Convert hex key to integer then to binary string of length 2
        val = int(k, 16)
        bitstring = format(val, '02b')
        probs[bitstring] = v / total_shots
        
    return probs
