# EVAL_META: task_id=31, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler


def sampler_qiskit():
    """Run a Bell circuit on Qiskit Runtime Sampler with an Aer simulator."""
    backend = AerSimulator(seed_simulator=42)
    sampler = Sampler(backend)

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    job = sampler.run([qc], shots=1024)
    result = job.result()

    counts = result[0].data.meas.get_counts()
    if isinstance(counts, list):
        counts = counts[0]

    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
