# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeManilaV2


def noisy_bell():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    fake_backend = FakeManilaV2()
    pm = generate_preset_pass_manager(optimization_level=1, backend=fake_backend)
    transpiled_qc = pm.run(qc)

    aer_backend = AerSimulator.from_backend(fake_backend)
    sampler = Sampler(mode=aer_backend)
    result = sampler.run([transpiled_qc]).result()

    pub_result = result[0]
    if hasattr(pub_result, "data") and hasattr(pub_result.data, "c"):
        return pub_result.data.c.get_probabilities()
    if hasattr(pub_result, "quasi_dists"):
        qd = pub_result.quasi_dists[0]
        return {format(k, "02b"): float(v) for k, v in qd.items()}
    if hasattr(pub_result, "quasi_dist"):
        qd = pub_result.quasi_dist
        return {format(k, "02b"): float(v) for k, v in qd.items()}
    return {}
