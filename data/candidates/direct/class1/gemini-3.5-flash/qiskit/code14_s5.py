# EVAL_META: task_id=14, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2

def bell_each_shot():
    # Create a Phi+ Bell circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Initialize Aer simulator backend
    backend = AerSimulator()
    
    # Transpile the circuit with preset pass manager at optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pm.run(qc)
    
    # Run using Qiskit Runtime Sampler V2 with the Aer simulator backend for 10 shots
    sampler = SamplerV2(backend=backend)
    job = sampler.run([transpiled_qc], shots=10)
    result = job.result()
    
    # Extract the classical register name and get counts
    pub_result = result[0]
    data = pub_result.data
    creg_name = transpiled_qc.cregs[0].name
    bit_array = getattr(data, creg_name)
    counts = bit_array.get_counts()
    
    # Convert counts to a probability distribution
    total_shots = sum(counts.values())
    prob_dist = {k: v / total_shots for k, v in counts.items()}
    
    return prob_dist
