# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def bell_each_shot():
    qc = QuantumCircuit(2, 2)
    qc.x(0)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    backend = AerSimulator()
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    transpiled_qc = pm.run(qc)

    sampler = Sampler(mode=backend)
    job = sampler.run([transpiled_qc], shots=10)
    result = job.result()

    pub_result = result[0]
    counts = pub_result.data.c.get_counts()
    total = sum(counts.values()) or 1
    return {bitstring: count / total for bitstring, count in counts.items()}
