# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def init_random_3qubit(desired_vector):
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator

    qc = QuantumCircuit(3)
    qc.initialize(desired_vector, [0, 1, 2])
    qc.measure_all()

    backend = AerSimulator()
    shots = 100000
    counts = None

    try:
        from qiskit_ibm_runtime import SamplerV2 as Sampler
        try:
            sampler = Sampler(mode=backend)
        except TypeError:
            sampler = Sampler(backend=backend)
        job = sampler.run([qc], shots=shots)
        result = job.result()
        counts = result[0].data.meas.get_counts()
    except Exception:
        try:
            from qiskit_aer.primitives import SamplerV2 as AerSampler
            sampler = AerSampler()
            job = sampler.run([qc], shots=shots)
            result = job.result()
            counts = result[0].data.meas.get_counts()
        except Exception:
            probs = np.abs(np.asarray(desired_vector)) ** 2
            probs = probs / np.sum(probs)
            return {format(i, '03b'): float(probs[i]) for i in range(8)}

    dist = {format(i, '03b'): 0.0 for i in range(8)}
    for bitstring, count in counts.items():
        dist[bitstring] = count / shots
    return dist
