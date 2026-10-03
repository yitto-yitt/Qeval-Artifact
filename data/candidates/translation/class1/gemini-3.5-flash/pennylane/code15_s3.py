# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml
from qiskit_ibm_runtime.fake_provider import FakeBelemV2
from qiskit_aer.noise import NoiseModel

def noisy_bell():
    device_backend = FakeBelemV2()
    noise_model = NoiseModel.from_backend(device_backend)
    coupling_map = device_backend.coupling_map
    basis_gates = device_backend.operation_names

    dev = qml.device(
        'qiskit.aer',
        wires=5,
        shots=1000,
        noise_model=noise_model,
        coupling_map=coupling_map,
        basis_gates=basis_gates
    )

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[0, 1])

    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
