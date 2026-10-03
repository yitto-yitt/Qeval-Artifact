# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml
from qiskit_ibm_runtime.fake_provider import FakeBelemV2
from qiskit_aer import AerSimulator

def noisy_bell():
    device_backend = FakeBelemV2()
    simulator = AerSimulator.from_backend(device_backend)
    
    dev = qml.device('qiskit.aer', wires=5, shots=1000, backend=simulator)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[1, 0])
    
    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
