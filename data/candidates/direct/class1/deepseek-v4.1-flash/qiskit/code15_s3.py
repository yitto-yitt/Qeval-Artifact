# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler


def noisy_bell():
    qr = QuantumRegister(2, "q")
    cr = ClassicalRegister(2, "meas")
    qc = QuantumCircuit(qr, cr)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure(qr, cr)

    fake_backend = FakeManilaV2()
    sim = AerSimulator.from_backend(fake_backend)

    pm = generate_preset_pass_manager(optimization_level=1, backend=sim)
    isa_qc = pm.run(qc)

    sampler = Sampler(mode=sim)
    job = sampler.run([isa_qc])
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
