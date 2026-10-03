# EVAL_META: task_id=1, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def run_bell_state_simulator():
    # Define a phi plus Bell state
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Transpile the circuit with a preset pass manager at optimization level 1
    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pm.run(qc)
    
    # Run it with Qiskit Runtime Sampler on an Aer simulator backend
    sampler = SamplerV2(backend=backend)
    job = sampler.run([isa_circuit])
    result = job.result()
    
    # Extract measurement results and calculate probability distribution
    pub_result = result[0]
    creg_name = isa_circuit.cregs[0].name
    counts = getattr(pub_result.data, creg_name).get_counts()
    
    total_shots = sum(counts.values())
    prob_dist = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return prob_dist
