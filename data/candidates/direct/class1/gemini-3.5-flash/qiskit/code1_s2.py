# EVAL_META: task_id=1, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler

def run_bell_state_simulator():
    # Define a phi plus Bell state
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    
    # Set up Aer simulator backend
    backend = AerSimulator()
    
    # Transpile the circuit with optimization level 1
    transpiled_qc = transpile(qc, backend=backend, optimization_level=1)
    
    # Run using Qiskit Runtime Sampler on the Aer backend
    sampler = Sampler(backend=backend)
    job = sampler.run(transpiled_qc)
    result = job.result()
    
    # Extract and return the probability distribution
    quasi_dist = result.quasi_dists[0]
    return quasi_dist.binary_probabilities()
