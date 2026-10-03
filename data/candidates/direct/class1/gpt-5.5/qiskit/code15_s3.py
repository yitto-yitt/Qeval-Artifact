# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
import qiskit_ibm_runtime.fake_provider as fake_provider

try:
    from qiskit_ibm_runtime import SamplerV2 as Sampler
except ImportError:
    from qiskit_ibm_runtime import Sampler


def noisy_bell():
    fake_backend_cls = getattr(fake_provider, "FakeManilaV2")
    fake_backend = fake_backend_cls()
    backend = AerSimulator.from_backend(fake_backend)

    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_circuit = pass_manager.run(circuit)

    shots = 4096
    sampler = Sampler(mode=backend)
    job = sampler.run([transpiled_circuit], shots=shots)
    result = job.result()

    counts = None
    try:
        data = result[0].data
        if hasattr(data, "meas"):
            counts = data.meas.get_counts()
        else:
            for name in data.keys():
                value = getattr(data, name)
                if hasattr(value, "get_counts"):
                    counts = value.get_counts()
                    break
    except Exception:
        counts = None

    if counts is None and hasattr(result, "quasi_dists"):
        quasi = result.quasi_dists[0]
        counts = {}
        for key, value in quasi.items():
            bitstring = format(key, "02b") if isinstance(key, int) else str(key)
            counts[bitstring] = float(value) * shots

    total = float(sum(counts.values()))
    distribution = {format(i, "02b"): counts.get(format(i, "02b"), 0) / total for i in range(4)}
    for bitstring, count in counts.items():
        distribution[bitstring] = count / total
    return distribution
