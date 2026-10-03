# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeManilaV2


def noisy_bell():
    fake_backend = FakeManilaV2()
    simulator = AerSimulator.from_backend(fake_backend)

    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    pm = generate_preset_pass_manager(optimization_level=1, backend=simulator)
    tqc = pm.run(qc)

    sampler = Sampler(mode=simulator)
    job = sampler.run([tqc], shots=4096)
    result = job.result()

    if hasattr(result, "quasi_dists"):
        dist = result.quasi_dists[0]
        return {format(k, "02b"): float(v) for k, v in dist.items()}

    pub_res = result[0]
    data = pub_res.data
    if hasattr(data, "c"):
        counts = data.c.get_counts()
    else:
        first_attr = next(iter(vars(data).keys()))
        counts = getattr(data, first_attr).get_counts()

    total = sum(counts.values()) or 1
    return {k: v / total for k, v in counts.items()}
