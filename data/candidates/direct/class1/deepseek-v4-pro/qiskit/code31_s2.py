# EVAL_META: task_id=31, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler


def sampler_qiskit():
    backend = AerSimulator()
    backend.set_options(seed_simulator=42)

    sampler = Sampler(backend=backend)

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    shots = 1024
    job = sampler.run([qc], shots=shots)
    result = job.result()

    data = result[0].data
    if hasattr(data, "meas"):
        counts = data.meas.get_counts()
    else:
        counts = data.c.get_counts()

    return {bitstring: count / shots for bitstring, count in counts.items()}
