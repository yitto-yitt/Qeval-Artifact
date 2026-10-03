# EVAL_META: task_id=31, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def sampler_qiskit():
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    backend = AerSimulator(seed_simulator=42)
    sampler = Sampler(mode=backend)

    job = sampler.run([circuit], shots=1024)
    result = job.result()[0]

    counts = result.data.meas.get_counts()
    total = sum(counts.values())

    return {bitstring: count / total for bitstring, count in sorted(counts.items())}
