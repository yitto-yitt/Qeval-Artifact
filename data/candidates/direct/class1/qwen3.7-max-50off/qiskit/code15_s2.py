# EVAL_META: task_id=15, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeGenericBackendV2
from qiskit_ibm_runtime import SamplerV2


def noisy_bell():
    fake_backend = FakeGenericBackendV2(num_qubits=5)
    aer_sim = AerSimulator.from_backend(fake_backend)

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    pm = generate_preset_pass_manager(optimization_level=1, backend=aer_sim)
    transpiled_qc = pm.run(qc)

    sampler = SamplerV2(mode=aer_sim)
    job = sampler.run([transpiled_qc], shots=1024)
    result = job.result()

    pub_result = result[0]
    counts = pub_result.data.meas.get_counts()
    total = sum(counts.values())
    prob_dist = {k: v / total for k, v in counts.items()}

    return prob_dist
