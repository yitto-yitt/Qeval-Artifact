# EVAL_META: task_id=14, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler

def bell_each_shot():
    # Create a Phi+ Bell circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Use Aer simulator backend
    backend = AerSimulator()
    
    # Transpile the circuit with optimization level 1
    qc_transpiled = transpile(qc, backend=backend, optimization_level=1)
    
    # Run using Qiskit Runtime Sampler for 10 shots
    sampler = Sampler(backend=backend)
    job = sampler.run(qc_transpiled, shots=10)
    result = job.result()
    
    # Get the probability distribution keyed by measurement bitstrings
    quasi_dist = result.quasi_dists[0]
    return quasi_dist.binary_probabilities()
