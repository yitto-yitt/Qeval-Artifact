# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def run_bell_state_simulator():
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    backend = AerSimulator()
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_circuit = pass_manager.run(circuit)

    sampler = SamplerV2(mode=backend)
    sampler.options.default_shots = 4096
    job = sampler.run([transpiled_circuit])
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
