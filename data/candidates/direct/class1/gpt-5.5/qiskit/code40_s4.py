# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def init_random_3qubit(desired_vector):
    if hasattr(desired_vector, "data") and not isinstance(desired_vector, (list, tuple, np.ndarray)):
        desired_vector = desired_vector.data

    vector = np.asarray(desired_vector, dtype=complex).reshape(-1)
    if vector.size != 8:
        raise ValueError("desired_vector must contain exactly 8 amplitudes for a 3-qubit state.")

    norm = np.linalg.norm(vector)
    if norm == 0:
        raise ValueError("desired_vector must not be the zero vector.")
    vector = vector / norm

    qr = QuantumRegister(3, "q")
    cr = ClassicalRegister(3, "m")
    circuit = QuantumCircuit(qr, cr)
    circuit.initialize(vector.tolist(), qr)
    circuit.measure(qr, cr)

    backend = AerSimulator(seed_simulator=12345)
    isa_circuit = transpile(circuit, backend=backend, seed_transpiler=12345, optimization_level=1)

    sampler = SamplerV2(mode=backend)
    shots = 32768
    job = sampler.run([isa_circuit], shots=shots)
    result = job.result()[0]
    counts = result.data.m.get_counts()

    total = sum(counts.values())
    return {f"{i:03b}": counts.get(f"{i:03b}", 0) / total for i in range(8)}
