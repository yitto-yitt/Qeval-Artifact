# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def init_random_3qubit(desired_vector):
    circuit = QuantumCircuit(3)
    circuit.initialize(desired_vector, range(3), normalize=True)
    circuit.measure_all()

    backend = AerSimulator(seed_simulator=42)
    circuit = transpile(circuit, backend, seed_transpiler=42)
    sampler = SamplerV2(mode=backend)
    result = sampler.run([circuit], shots=16384).result()
    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())

    return {
        format(index, "03b"): counts.get(format(index, "03b"), 0) / total
        for index in range(8)
    }
