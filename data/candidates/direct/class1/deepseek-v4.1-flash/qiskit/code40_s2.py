# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

def init_random_3qubit(desired_vector):
    if hasattr(desired_vector, 'data'):
        vec = np.asarray(desired_vector.data, dtype=complex)
    else:
        vec = np.asarray(desired_vector, dtype=complex)
    vec = vec / np.linalg.norm(vec)
    
    qc = QuantumCircuit(3)
    try:
        qc.prepare_state(vec, [0, 1, 2])
    except AttributeError:
        qc.initialize(vec, [0, 1, 2])
    
    creg = ClassicalRegister(3, 'meas')
    qc.add_register(creg)
    qc.measure([0, 1, 2], creg)
    
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    shots = 100000
    job = sampler.run([qc], shots=shots)
    result = job.result()
    counts = result[0].data.meas.get_counts()
    
    probs = {format(i, '03b'): 0.0 for i in range(8)}
    for bitstring, count in counts.items():
        probs[bitstring] = count / shots
    return probs
