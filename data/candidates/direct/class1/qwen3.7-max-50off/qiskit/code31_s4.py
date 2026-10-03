# EVAL_META: task_id=31, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler

def sampler_qiskit():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    
    backend = AerSimulator(seed_simulator=42)
    sampler = Sampler(backend=backend)
    
    job = sampler.run([qc])
    result = job.result()
    
    counts = result[0].data.c.get_counts()
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}
    
    return probs
