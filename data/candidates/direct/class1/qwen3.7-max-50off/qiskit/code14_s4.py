# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2


def bell_each_shot():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    backend = AerSimulator()

    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled = pm.run(qc)

    sampler = SamplerV2(backend)
    job = sampler.run([transpiled], shots=10)
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
