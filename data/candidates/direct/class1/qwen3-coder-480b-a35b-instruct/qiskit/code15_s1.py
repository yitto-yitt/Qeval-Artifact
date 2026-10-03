# EVAL_META: task_id=15, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import Sampler
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeManila


def noisy_bell():
    # Create Bell circuit
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    
    # Get fake backend and create Aer simulator
    fake_backend = FakeManila()
    aer_sim = AerSimulator.from_backend(fake_backend)
    
    # Generate preset pass manager at optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=aer_sim)
    
    # Transpile circuit
    transpiled_qc = pm.run(qc)
    
    # Run with Sampler
    sampler = Sampler(backend=aer_sim)
    job = sampler.run([transpiled_qc])
    result = job.result()
    
    # Return probability distribution
    return result.quasi_dists[0].binary_probabilities()
