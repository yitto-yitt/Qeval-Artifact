# EVAL_META: task_id=14, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2

def bell_each_shot():
    # Create a Phi+ Bell circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Aer simulator backend
    backend = AerSimulator()
    
    # Transpile the circuit with a preset pass manager at optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pm.run(qc)
    
    # Run using Qiskit Runtime Sampler for 10 shots
    sampler = SamplerV2(backend=backend)
    job = sampler.run([transpiled_qc], shots=10)
    result = job.result()
    
    # Get the pub result
    pub_result = result[0]
    
    # Extract counts
    try:
        keys = list(pub_result.data.keys())
        creg_name = keys[0]
    except Exception:
        creg_name = 'meas'
        
    creg_data = getattr(pub_result.data, creg_name)
    counts = creg_data.get_counts()
    
    # Calculate probability distribution
    total_shots = sum(counts.values())
    prob_dist = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return prob_dist
