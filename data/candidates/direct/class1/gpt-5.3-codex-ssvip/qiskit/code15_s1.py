# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit_ibm_runtime import SamplerV2 as Sampler


def noisy_bell():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    fake_backend = FakeManilaV2()
    sim = AerSimulator.from_backend(fake_backend)

    pm = generate_preset_pass_manager(backend=sim, optimization_level=1)
    tqc = pm.run(qc)

    sampler = Sampler(mode=sim)
    job = sampler.run([tqc])
    result = job.result()

    pub_res = result[0]
    data = pub_res.data

    if hasattr(data, "meas"):
        quasi = data.meas.get_counts()
    elif hasattr(data, "c"):
        quasi = data.c.get_counts()
    else:
        quasi = {}

    total = sum(quasi.values()) if quasi else 0
    if total == 0:
        return {}
    return {k: v / total for k, v in quasi.items()}
