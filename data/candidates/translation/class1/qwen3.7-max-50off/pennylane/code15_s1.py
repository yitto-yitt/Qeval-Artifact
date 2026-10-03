# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml
from qiskit_ibm_runtime.fake_provider import FakeBelemV2
from qiskit_aer.noise import NoiseModel

def noisy_bell():
    backend = FakeBelemV2()
    noise_model = NoiseModel.from_backend(backend)
    dev = qml.device("qiskit.aer", wires=2, shots=1000, noise_model=noise_model)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[0, 1])
        
    counts = circuit()
    total = sum(counts.values())
    probs = {}
    for k, v in counts.items():
        if isinstance(k, int):
            k = format(k, '02b')
        elif isinstance(k, tuple):
            k = "".join(str(b) for b in k)
        probs[k] = v / total
    return probs
