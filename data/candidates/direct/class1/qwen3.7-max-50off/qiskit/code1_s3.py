# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def run_bell_state_simulator():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    backend = AerSimulator()
    transpiled = transpile(qc, backend=backend, optimization_level=1)

    sampler = Sampler(mode=backend)
    job = sampler.run([transpiled])
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
