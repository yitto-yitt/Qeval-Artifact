# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler


def bell_each_shot():
    # Build phi+ Bell circuit (|00> + |11>)/sqrt(2) with measurements
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure(range(2), range(2))

    # Use Aer simulator as backend
    backend = AerSimulator()

    # Transpile with preset pass manager at optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled = pm.run(qc)

    # Run with Qiskit Runtime Sampler (local Aer backend)
    sampler = Sampler(backend=backend)
    job = sampler.run(transpiled, shots=10)
    result = job.result()

    # Extract quasi-distribution and convert keys to two-bit strings
    quasi_dist = result.quasi_dists[0]
    prob_dist = {format(k, "b").zfill(2): v for k, v in quasi_dist.items()}

    return prob_dist
