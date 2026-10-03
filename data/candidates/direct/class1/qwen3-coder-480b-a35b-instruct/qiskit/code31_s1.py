# EVAL_META: task_id=31, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler


def sampler_qiskit():
    # Create Bell circuit
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    
    # Create Aer simulator with seed
    backend = AerSimulator(seed_simulator=42)
    
    # Create sampler and run circuit
    sampler = Sampler(backend)
    job = sampler.run(qc, shots=1000)
    result = job.result()
    
    # Return probability distribution
    return result.quasi_dists[0]
