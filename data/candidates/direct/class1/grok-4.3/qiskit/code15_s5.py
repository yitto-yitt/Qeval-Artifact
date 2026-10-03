# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeManila

def noisy_bell():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    fake_backend = FakeManila()
    backend = AerSimulator.from_backend(fake_backend)
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_qc = pm.run(qc)
    sampler = Sampler(backend=backend)
    job = sampler.run([isa_qc])
    result = job.result()
    counts = result[0].data.meas.get_counts()
    shots = sum(counts.values())
    return {k: v / shots for k, v in counts.items()}
