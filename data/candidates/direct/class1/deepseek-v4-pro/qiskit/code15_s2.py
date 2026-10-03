# EVAL_META: task_id=15, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit_ibm_runtime.fake_provider import FakeManilaV2


def noisy_bell():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    backend = AerSimulator.from_backend(FakeManilaV2())
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pass_manager.run(qc)

    sampler = Sampler(backend=backend)
    job = sampler.run([isa_circuit], shots=1024)
    result = job.result()

    counts = result.data[0].meas.get_counts()
    total_shots = sum(counts.values())
    return {bitstring: count / total_shots for bitstring, count in counts.items()}
