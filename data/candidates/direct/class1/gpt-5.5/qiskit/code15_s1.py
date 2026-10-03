# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeManilaV2


def noisy_bell():
    shots = 1024

    qreg = QuantumRegister(2, "q")
    creg = ClassicalRegister(2, "meas")
    circuit = QuantumCircuit(qreg, creg)
    circuit.h(qreg[0])
    circuit.cx(qreg[0], qreg[1])
    circuit.measure(qreg, creg)

    fake_backend = FakeManilaV2()
    simulator = AerSimulator.from_backend(fake_backend)
    simulator.set_options(seed_simulator=15)

    pass_manager = generate_preset_pass_manager(
        optimization_level=1,
        backend=simulator,
        seed_transpiler=15,
    )
    transpiled_circuit = pass_manager.run(circuit)

    sampler = Sampler(mode=simulator)
    job = sampler.run([transpiled_circuit], shots=shots)
    result = job.result()

    pub_result = result[0]
    counts = pub_result.data.meas.get_counts()
    total = sum(counts.values())

    return {bitstring: count / total for bitstring, count in counts.items()}
