# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2
from qiskit_ibm_runtime.fake_provider import FakeManilaV2


def noisy_bell():
    simulator = AerSimulator.from_backend(FakeManilaV2())
    simulator.set_options(seed_simulator=42)

    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    pass_manager = generate_preset_pass_manager(
        optimization_level=1,
        backend=simulator,
        seed_transpiler=42,
    )
    isa_circuit = pass_manager.run(circuit)

    sampler = SamplerV2(mode=simulator)
    result = sampler.run([isa_circuit], shots=4096).result()
    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
