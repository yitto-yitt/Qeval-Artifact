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
    simulator = AerSimulator.from_backend(fake_backend)

    pm = generate_preset_pass_manager(optimization_level=1, backend=simulator)
    tqc = pm.run(qc)

    sampler = Sampler(mode=simulator)
    result = sampler.run([tqc]).result()
    pub_result = result[0]
    return pub_result.data.c.get_counts()
