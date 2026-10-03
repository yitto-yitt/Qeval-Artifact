# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def run_bell_state_simulator():
    shots = 4096

    qreg = QuantumRegister(2, "q")
    creg = ClassicalRegister(2, "meas")
    circuit = QuantumCircuit(qreg, creg)

    circuit.h(qreg[0])
    circuit.cx(qreg[0], qreg[1])
    circuit.measure(qreg, creg)

    backend = AerSimulator(seed_simulator=12345)
    pass_manager = generate_preset_pass_manager(
        optimization_level=1,
        backend=backend,
        seed_transpiler=12345,
    )
    transpiled_circuit = pass_manager.run(circuit)

    sampler = Sampler(mode=backend)
    result = sampler.run([transpiled_circuit], shots=shots).result()

    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())

    return {bitstring: count / total for bitstring, count in sorted(counts.items())}
