# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit_ibm_runtime import SamplerV2


def noisy_bell():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    fake_backend = FakeManilaV2()
    backend = AerSimulator.from_backend(fake_backend)

    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pm.run(qc)

    sampler = SamplerV2(mode=backend)
    job = sampler.run([isa_circuit])
    result = job.result()

    counts = result[0].data.c.get_counts()
    shots = sum(counts.values())
    return {bitstring: count / shots for bitstring, count in counts.items()}
