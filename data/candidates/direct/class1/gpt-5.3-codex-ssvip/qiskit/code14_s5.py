# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def bell_each_shot():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.s(0)
    qc.measure([0, 1], [0, 1])

    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    tqc = pm.run(qc)

    sampler = Sampler(mode=backend)
    job = sampler.run([tqc], shots=10)
    result = job.result()
    pub_result = result[0]
    counts = pub_result.data.c.get_counts()

    total = sum(counts.values()) if counts else 0
    if total == 0:
        return {}
    return {k: v / total for k, v in counts.items()}
