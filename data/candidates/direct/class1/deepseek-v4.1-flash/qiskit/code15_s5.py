# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2
from qiskit_ibm_runtime.fake_provider import FakeManila


def noisy_bell():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    fake_backend = FakeManila()
    pm = generate_preset_pass_manager(optimization_level=1, backend=fake_backend)
    transpiled_qc = pm.run(qc)

    sim = AerSimulator.from_backend(fake_backend)
    sampler = SamplerV2(mode=sim)
    shots = 1024
    job = sampler.run([transpiled_qc], shots=shots)
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
