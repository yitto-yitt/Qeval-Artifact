# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def init_random_3qubit(desired_vector):
    circuit = QuantumCircuit(3)
    circuit.initialize(desired_vector, [0, 1, 2], normalize=True)
    circuit.measure_all()

    backend = AerSimulator()
    compiled_circuit = transpile(circuit, backend)
    sampler = SamplerV2(mode=backend)
    result = sampler.run([compiled_circuit], shots=8192).result()
    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())

    return {format(i, "03b"): counts.get(format(i, "03b"), 0) / total for i in range(8)}
