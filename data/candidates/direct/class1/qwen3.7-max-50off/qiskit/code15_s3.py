# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit_ibm_runtime import SamplerV2 as Sampler


def noisy_bell():
    fake_backend = FakeManilaV2()
    simulator = AerSimulator.from_backend(fake_backend)

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    pm = generate_preset_pass_manager(optimization_level=1, backend=simulator)
    transpiled_qc = pm.run(qc)

    sampler = Sampler(mode=simulator)
    job = sampler.run([transpiled_qc])
    result = job.result()

    pub_result = result[0]
    counts = pub_result.data.meas.get_counts()
    total_shots = sum(counts.values())
    prob_dist = {k: v / total_shots for k, v in counts.items()}

    return prob_dist
