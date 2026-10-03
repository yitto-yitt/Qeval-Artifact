# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def noisy_bell():
    from qiskit_ibm_runtime.fake_provider import FakeBelemV2
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel

    device_backend = FakeBelemV2()
    simulator = AerSimulator.from_backend(device_backend)
    noise_model = NoiseModel.from_backend(device_backend)

    basis_gates = noise_model.basis_gates
    coupling_map = device_backend.coupling_map

    dev = qml.device(
        "qiskit.aer",
        wires=2,
        noise_model=noise_model,
        optimization_level=1,
        shots=1000,
    )

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    samples = circuit()

    counts = {}
    for sample in samples:
        key = "".join(str(int(b)) for b in sample)
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
