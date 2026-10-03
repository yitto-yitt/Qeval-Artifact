# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def init_random_3qubit(desired_vector):
    circuit = QuantumCircuit(3)
    circuit.initialize(desired_vector, [0, 1, 2], normalize=True)
    circuit.measure_all()

    backend = AerSimulator()
    circuit = transpile(circuit, backend)
    sampler = SamplerV2(mode=backend)
    result = sampler.run([circuit], shots=10000).result()
    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())

    return {bitstring: count / total for bitstring, count in counts.items()}
