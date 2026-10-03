# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit_ibm_runtime.fake_provider import FakeManila


def noisy_bell():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    backend = AerSimulator.from_backend(FakeManila())

    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_qc = pm.run(qc)

    sampler = Sampler(mode=backend)
    job = sampler.run([isa_qc], shots=1024)
    result = job.result()

    quasi_dist = result.quasi_dists[0]

    if hasattr(quasi_dist, "binary_probabilities"):
        return quasi_dist.binary_probabilities()

    return {
        key if isinstance(key, str) else format(key, "b").zfill(qc.num_clbits): prob
        for key, prob in quasi_dist.items()
    }
