# EVAL_META: task_id=15, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit_ibm_runtime import SamplerV2

def noisy_bell():
    # Create a Bell circuit
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    
    # Create Aer simulator from a fake backend
    fake_backend = FakeManilaV2()
    backend = AerSimulator.from_backend(fake_backend)
    
    # Transpile using a preset pass manager at optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pm.run(qc)
    
    # Run with Qiskit Runtime Sampler
    sampler = SamplerV2(backend=backend)
    job = sampler.run([transpiled_qc])
    result = job.result()
    
    # Extract probability distribution
    pub_result = result[0]
    creg_name = transpiled_qc.cregs[0].name
    counts = getattr(pub_result.data, creg_name).get_counts()
    
    total_shots = sum(counts.values())
    prob_dist = {k: v / total_shots for k, v in counts.items()}
    
    return prob_dist
