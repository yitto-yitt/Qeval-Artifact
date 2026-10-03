# EVAL_META: task_id=15, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit_ibm_runtime.fake_provider import FakeVigo

def noisy_bell():
    # Create Bell circuit with measurement
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    # Create Aer simulator from fake backend
    fake_backend = FakeVigo()
    backend = AerSimulator.from_backend(fake_backend)

    # Transpile at optimization level 1 using preset pass manager
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pm.run(qc)

    # Run with Runtime Sampler (local mode)
    sampler = Sampler(backend=backend)
    job = sampler.run([transpiled_qc])
    result = job.result()

    # Extract quasi-probability distribution and convert int keys to bitstrings
    quasi_dist = result.quasi_dists[0]
    bitstring_dist = {format(k, '02b'): v for k, v in quasi_dist.items()}

    return bitstring_dist
