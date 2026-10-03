# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml
from qiskit_ibm_runtime.fake_provider import FakeBelemV2
from qiskit_aer.noise import NoiseModel

def noisy_bell():
    backend = FakeBelemV2()
    noise_model = NoiseModel.from_backend(backend)
    coupling_map = backend.coupling_map
    basis_gates = backend.operation_names

    dev = qml.device(
        'qiskit.aer',
        wires=5,
        shots=1000,
        noise_model=noise_model,
        coupling_map=coupling_map,
        basis_gates=basis_gates,
        optimization_level=1
    )

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[0, 1])

    counts = circuit()
    total = sum(counts.values())
    
    prob_dist = {}
    for key, val in counts.items():
        if isinstance(key, tuple):
            key_str = "".join(str(b) for b in key)
        else:
            key_str = str(key)
        prob_dist[key_str] = val / total
        
    return prob_dist
