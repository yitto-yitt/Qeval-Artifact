# EVAL_META: task_id=1, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler


def run_bell_state_simulator():
    # Create quantum circuit for Phi+ Bell state
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    
    # Transpile with optimization level 1
    backend = AerSimulator()
    transpiled_qc = transpile(qc, backend, optimization_level=1)
    
    # Run with Sampler
    sampler = Sampler(backend)
    job = sampler.run([transpiled_qc], shots=1000)
    result = job.result()
    
    # Return probability distribution
    return result.quasi_dists[0].binary_probabilities()
