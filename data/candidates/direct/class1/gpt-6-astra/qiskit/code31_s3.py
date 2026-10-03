# EVAL_META: task_id=31, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def sampler_qiskit():
    backend = AerSimulator(seed_simulator=42)

    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()
    circuit = transpile(circuit, backend, seed_transpiler=42)

    sampler = SamplerV2(
        mode=backend,
        options={"simulator": {"seed_simulator": 42}},
    )
    result = sampler.run([circuit], shots=1024).result()
    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
