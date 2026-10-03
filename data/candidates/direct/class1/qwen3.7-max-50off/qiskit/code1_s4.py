# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler


def run_bell_state_simulator():
    # Create phi plus Bell state: |Φ+⟩ = (|00⟩ + |11⟩) / √2
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    # Set up Aer simulator backend
    backend = AerSimulator()

    # Transpile with preset pass manager at optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled = pm.run(qc)

    # Run with Qiskit Runtime Sampler
    sampler = Sampler(backend=backend)
    job = sampler.run([transpiled], shots=1024)
    result = job.result()

    # Extract counts and convert to probability distribution
    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    probs = {bitstring: count / total for bitstring, count in counts.items()}

    return probs
