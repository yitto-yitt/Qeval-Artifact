# EVAL_META: task_id=31, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2

def sampler_qiskit():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    backend = AerSimulator(seed_simulator=42)
    sampler = SamplerV2(mode=backend)
    job = sampler.run([qc], shots=1024)
    result = job.result()
    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    return {bitstr: count / total for bitstr, count in counts.items()}
