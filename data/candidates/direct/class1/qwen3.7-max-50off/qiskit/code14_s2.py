# EVAL_META: task_id=14, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler


def bell_each_shot():
    # Create phi plus Bell state circuit: |Φ+⟩ = (|00⟩ + |11⟩)/√2
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    # Aer simulator backend
    backend = AerSimulator()

    # Transpile with preset pass manager at optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pm.run(qc)

    # Run with Qiskit Runtime Sampler for 10 shots
    sampler = Sampler(backend=backend)
    job = sampler.run([isa_circuit], shots=10)
    result = job.result()

    # Extract probability distribution from measurement results
    pub_result = result[0]
    bit_array = pub_result.data.meas
    counts = bit_array.get_counts()
    total_shots = sum(counts.values())
    prob_dist = {bitstring: count / total_shots for bitstring, count in counts.items()}

    return prob_dist
