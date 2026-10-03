# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as RuntimeSampler
from qiskit.primitives import BackendSamplerV2


def run_bell_state_simulator():
    shots = 8192

    circuit = QuantumCircuit(2, name="phi_plus_bell")
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    backend = AerSimulator(seed_simulator=12345)
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_circuit = pass_manager.run(circuit)

    try:
        sampler = RuntimeSampler(mode=backend)
        job = sampler.run([transpiled_circuit], shots=shots)
        result = job.result()
    except Exception:
        sampler = BackendSamplerV2(backend=backend)
        job = sampler.run([transpiled_circuit], shots=shots)
        result = job.result()

    data = result[0].data
    if hasattr(data, "meas"):
        counts = data.meas.get_counts()
    else:
        counts = next(iter(data.values())).get_counts()

    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
