# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def bell_each_shot():
    shots = 10
    backend = AerSimulator(seed_simulator=14)

    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])

    pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=1)
    transpiled_circuit = pass_manager.run(circuit)

    sampler = Sampler(mode=backend)
    job = sampler.run([transpiled_circuit], shots=shots)
    result = job.result()[0]

    counts = result.data.c.get_counts()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
