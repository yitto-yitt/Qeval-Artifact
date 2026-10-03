# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2

def run_bell_state_simulator():
    # Phi+ Bell state: (|00> + |11>) / sqrt(2)
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    backend = AerSimulator()

    # Transpile using preset pass manager at optimization level 1
    transpiled_qc = transpile(qc, backend=backend, optimization_level=1)

    # Run with Qiskit Runtime Sampler on Aer simulator
    sampler = SamplerV2(backend=backend)
    job = sampler.run([transpiled_qc], shots=1024)
    result = job.result()

    counts = result[0].data.c.get_counts()
    total_shots = sum(counts.values())

    return {bits: count / total_shots for bits, count in sorted(counts.items())}
