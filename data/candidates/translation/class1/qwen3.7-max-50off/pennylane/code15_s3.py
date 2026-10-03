# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml

def noisy_bell():
    try:
        from qiskit_ibm_runtime.fake_provider import FakeBelemV2
        from qiskit_aer.noise import NoiseModel
        backend = FakeBelemV2()
        noise_model = NoiseModel.from_backend(backend)
        dev = qml.device("qiskit.aer", wires=2, shots=1000, noise_model=noise_model)
    except Exception:
        dev = qml.device("default.qubit", wires=2, shots=1000)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[0, 1])

    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
