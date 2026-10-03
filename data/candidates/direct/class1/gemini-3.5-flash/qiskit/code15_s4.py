# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeManila

def noisy_bell():
    # Create a Bell circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Fake backend and Aer simulator
    fake_backend = FakeManila()
    aer_sim = AerSimulator.from_backend(fake_backend)
    
    # Transpile using preset pass manager at optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=aer_sim)
    transpiled_qc = pm.run(qc)
    
    # Run with Qiskit Runtime Sampler
    sampler = Sampler(backend=aer_sim)
    job = sampler.run([transpiled_qc])
    result = job.result()
    
    # Get the counts from the classical register
    pub_result = result[0]
    creg_name = qc.cregs[0].name
    counts = getattr(pub_result.data, creg_name).get_counts()
    
    # Convert counts to probability distribution
    total_shots = sum(counts.values())
    probabilities = {bitstr: count / total_shots for bitstr, count in counts.items()}
    
    return probabilities
