# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def init_random_3qubit(desired_vector):
    state = np.asarray(desired_vector, dtype=complex).reshape(-1)
    if state.size != 8 or not np.all(np.isfinite(state)):
        raise ValueError("desired_vector must contain eight finite amplitudes.")

    scale = np.max(np.abs(state))
    if scale == 0:
        raise ValueError("desired_vector must have nonzero norm.")
    state = state / scale
    state = state / np.linalg.norm(state)

    circuit = QuantumCircuit(3)
    circuit.initialize(state, [0, 1, 2])
    circuit.measure_all()

    backend = AerSimulator()
    circuit = transpile(circuit, backend)
    sampler = SamplerV2(mode=backend)
    result = sampler.run([circuit], shots=16384).result()
    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())

    return {format(i, "03b"): counts.get(format(i, "03b"), 0) / total for i in range(8)}
