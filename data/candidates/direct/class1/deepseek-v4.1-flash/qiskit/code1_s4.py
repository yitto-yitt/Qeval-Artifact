# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

def run_bell_state_simulator():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pm.run(qc)

    sampler = Sampler(mode=backend)
    job = sampler.run([isa_circuit])
    result = job.result()
    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
