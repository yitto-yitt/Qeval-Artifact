# EVAL_META: task_id=15, framework=qiskit, class=1
import importlib

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

try:
    from qiskit_ibm_runtime import SamplerV2 as Sampler
except ImportError:
    from qiskit_ibm_runtime import Sampler


def noisy_bell():
    fake_backend = None

    try:
        fake_provider = importlib.import_module("qiskit_ibm_runtime.fake_provider")
        for name in ("FakeManilaV2", "FakeLimaV2", "FakeBelemV2", "FakeQuitoV2", "FakeVigoV2"):
            cls = getattr(fake_provider, name, None)
            if cls is not None:
                try:
                    fake_backend = cls()
                    break
                except Exception:
                    pass

        if fake_backend is None:
            for name in dir(fake_provider):
                if not name.startswith("Fake") or "Provider" in name:
                    continue
                cls = getattr(fake_provider, name)
                if not isinstance(cls, type):
                    continue
                try:
                    candidate = cls()
                    num_qubits = getattr(candidate, "num_qubits", 0)
                    if 2 <= num_qubits <= 7:
                        fake_backend = candidate
                        break
                except Exception:
                    pass
    except Exception:
        pass

    if fake_backend is None:
        generic_provider = importlib.import_module("qiskit.providers.fake_provider")
        GenericBackendV2 = getattr(generic_provider, "GenericBackendV2")
        try:
            fake_backend = GenericBackendV2(
                2,
                basis_gates=["id", "rz", "sx", "x", "cx"],
                coupling_map=[[0, 1]],
                seed=12345,
            )
        except TypeError:
            fake_backend = GenericBackendV2(2)

    simulator = AerSimulator.from_backend(fake_backend)
    simulator.set_options(seed_simulator=12345)

    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=simulator)
    transpiled_circuit = pass_manager.run(circuit)

    sampler = Sampler(mode=simulator)
    job = sampler.run([transpiled_circuit], shots=4096)
    result = job.result()

    counts = result[0].data.meas.get_counts()
    counts = {str(key).replace(" ", ""): int(value) for key, value in counts.items()}
    shots = sum(counts.values())

    distribution = {format(i, "02b"): counts.get(format(i, "02b"), 0) / shots for i in range(4)}
    for key, value in counts.items():
        if key not in distribution:
            distribution[key] = value / shots

    return distribution
