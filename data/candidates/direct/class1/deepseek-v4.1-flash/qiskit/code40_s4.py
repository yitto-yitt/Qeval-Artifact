# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

def init_random_3qubit(desired_vector):
    vec = np.asarray(desired_vector, dtype=complex)
    vec = vec / np.linalg.norm(vec)
    
    qc = QuantumCircuit(3)
    qc.initialize(vec, qc.qubits)
    
    cr = ClassicalRegister(3, 'meas')
    qc.add_register(cr)
    qc.measure(range(3), cr)
    
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    job = sampler.run([qc], shots=100000)
    result = job.result()
    counts = result[0].data.meas.get_counts()
    
    total = sum(counts.values())
    all_keys = [format(i, '03b') for i in range(8)]
    probs = {key: 0.0 for key in all_keys}
    for key, val in counts.items():
        probs[key] = val / total
    return probs
