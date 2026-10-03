# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler


def run_bell_state_simulator():
    # Create phi plus Bell state: (|00> + |11>) / sqrt(2)
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    # Set up Aer simulator backend
    backend = AerSimulator()

    # Transpile with preset pass manager at optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled = pm.run(qc)

    # Run with Qiskit Runtime Sampler on the Aer simulator
    sampler = Sampler(mode=backend)
    job = sampler.run([transpiled])
    result = job.result()

    # Extract probability distribution from measurement results
    counts = result[0].data.meas.get_counts()
    total_shots = sum(counts.values())
    probabilities = {
        bitstring: count / total_shots for bitstring, count in counts.items()
    }

    return probabilities
