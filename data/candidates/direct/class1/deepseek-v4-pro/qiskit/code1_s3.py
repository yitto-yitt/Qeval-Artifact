# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler

def run_bell_state_simulator():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    backend = AerSimulator()
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pass_manager.run(qc)

    sampler = Sampler(backend=backend)
    job = sampler.run([isa_circuit], shots=1024)
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total_shots = sum(counts.values())
    return {bitstring: count / total_shots for bitstring, count in counts.items()}
