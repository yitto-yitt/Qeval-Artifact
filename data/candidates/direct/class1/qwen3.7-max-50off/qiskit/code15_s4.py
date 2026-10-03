# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def noisy_bell():
    fake_backend = GenericBackendV2(num_qubits=5, seed=42)
    aer_sim = AerSimulator.from_backend(fake_backend)

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    transpiled = transpile(qc, aer_sim, optimization_level=1)

    sampler = SamplerV2(mode=aer_sim)
    job = sampler.run([transpiled])
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
