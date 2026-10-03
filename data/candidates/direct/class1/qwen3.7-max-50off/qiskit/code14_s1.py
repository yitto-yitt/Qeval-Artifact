# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


def bell_each_shot():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    pm = generate_preset_pass_manager(optimization_level=1)
    transpiled = pm.run(qc)

    backend = AerSimulator()
    sampler = SamplerV2(mode=backend)
    job = sampler.run([transpiled], shots=10)
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    prob_dist = {k: v / total for k, v in counts.items()}

    return prob_dist
