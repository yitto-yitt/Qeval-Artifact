# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit_ibm_runtime.fake_provider import FakeManilaV2


def noisy_bell():
    backend = FakeManilaV2()
    sim_backend = AerSimulator.from_backend(backend)

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    pm = generate_preset_pass_manager(optimization_level=1, backend=sim_backend)
    isa_circuit = pm.run(qc)

    sampler = Sampler(backend=sim_backend)
    job = sampler.run([isa_circuit], shots=1024)
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())

    return {bitstring: count / total for bitstring, count in counts.items()}
