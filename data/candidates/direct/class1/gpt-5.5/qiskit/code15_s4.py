# EVAL_META: task_id=15, framework=qiskit, class=1
import qiskit_ibm_runtime.fake_provider as fake_provider
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def noisy_bell():
    fake_backend = None
    for backend_name in (
        "FakeManilaV2",
        "FakeLimaV2",
        "FakeJakartaV2",
        "FakeNairobiV2",
        "FakeQuitoV2",
        "FakeBelemV2",
        "FakeBrisbane",
        "FakeKyiv",
        "FakeSherbrooke",
    ):
        backend_cls = getattr(fake_provider, backend_name, None)
        if backend_cls is not None:
            fake_backend = backend_cls()
            break

    if fake_backend is None:
        raise RuntimeError("No suitable fake backend is available.")

    simulator = AerSimulator.from_backend(fake_backend)
    simulator.set_options(seed_simulator=12345)

    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    pass_manager = generate_preset_pass_manager(
        optimization_level=1,
        backend=simulator,
    )
    transpiled_circuit = pass_manager.run(circuit)

    sampler = Sampler(mode=simulator)
    job = sampler.run([transpiled_circuit], shots=1024)
    result = job.result()

    data = result[0].data
    if hasattr(data, "meas"):
        counts = data.meas.get_counts()
    elif hasattr(data, "c"):
        counts = data.c.get_counts()
    else:
        counts = None
        for _, datum in data.items():
            if hasattr(datum, "get_counts"):
                counts = datum.get_counts()
                break
        if counts is None:
            raise RuntimeError("No measurement counts found in sampler result.")

    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in sorted(counts.items())}
