# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def bell_each_shot():
    backend = AerSimulator(seed_simulator=14)

    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_circuit = pass_manager.run(circuit)

    sampler = Sampler(mode=backend)
    result = sampler.run([transpiled_circuit], shots=10).result()
    counts = result[0].data.meas.get_counts()

    return {bitstring: count / 10 for bitstring, count in counts.items()}
