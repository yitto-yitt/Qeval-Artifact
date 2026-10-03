# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit_ibm_runtime.fake_provider import FakeBelemV2

def noisy_bell():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    fake = FakeBelemV2()
    backend = AerSimulator.from_backend(fake)
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pm.run(qc)
    sampler = Sampler(backend=backend)
    job = sampler.run([isa_circuit], shots=1024)
    result = job.result()
    quasi = result.quasi_dists[0]
    return {format(int(k), "02b"): float(v) for k, v in quasi.items()}
