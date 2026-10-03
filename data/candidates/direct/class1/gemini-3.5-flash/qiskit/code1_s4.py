# EVAL_META: task_id=1, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2

def run_bell_state_simulator():
    # Define a Phi+ Bell state
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Initialize Aer simulator backend
    backend = AerSimulator()
    
    # Transpile the circuit with a preset pass manager at optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pm.run(qc)
    
    # Run using Qiskit Runtime SamplerV2 on the Aer simulator backend
    sampler = SamplerV2(backend=backend)
    job = sampler.run([transpiled_qc])
    result = job.result()
    
    # Extract measurement results
    pub_result = result[0]
    creg_data = pub_result.data.meas
    counts = creg_data.get_counts()
    
    # Calculate probability distribution
    total_shots = sum(counts.values())
    probabilities = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return probabilities
