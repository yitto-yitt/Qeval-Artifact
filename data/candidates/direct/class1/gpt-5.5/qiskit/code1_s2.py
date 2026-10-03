# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def run_bell_state_simulator():
    shots = 4096

    qr = QuantumRegister(2, "q")
    cr = ClassicalRegister(2, "meas")
    circuit = QuantumCircuit(qr, cr)
    circuit.h(qr[0])
    circuit.cx(qr[0], qr[1])
    circuit.measure(qr, cr)

    backend = AerSimulator(seed_simulator=12345)
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_circuit = pass_manager.run(circuit)

    sampler = Sampler(mode=backend)
    job = sampler.run([transpiled_circuit], shots=shots)
    result = job.result()[0]
    counts = result.data.meas.get_counts()

    return {bitstring: count / shots for bitstring, count in counts.items()}
