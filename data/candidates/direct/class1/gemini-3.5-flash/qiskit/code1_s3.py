# EVAL_META: task_id=1, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2

def run_bell_state_simulator():
    # Define a phi plus Bell state
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Initialize Aer simulator backend
    backend = AerSimulator()
    
    # Transpile the circuit with a preset pass manager at optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_circuit = pm.run(qc)
    
    # Run with Qiskit Runtime Sampler
    sampler = SamplerV2(backend=backend)
    job = sampler.run([transpiled_circuit])
    result = job.result()
    
    # Extract measurement results and calculate probabilities
    pub_result = result[0]
    counts = pub_result.data.meas.get_counts()
    
    total_shots = sum(counts.values())
    probabilities = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return probabilities
