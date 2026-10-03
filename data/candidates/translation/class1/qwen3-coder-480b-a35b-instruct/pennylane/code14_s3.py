# EVAL_META: task_id=14, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def bell_each_shot():
    dev = qml.device("default.qubit", wires=2, shots=10)
    
    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(qml.PauliZ(wires=0)), qml.sample(qml.PauliZ(wires=1))
    
    samples = bell_circuit()
    # Convert samples to bitstrings (Z eigenvalues to bit values)
    bitstrings = []
    for shot in range(samples[0].shape[0]):
        bit0 = '0' if samples[0][shot] == 1 else '1'
        bit1 = '0' if samples[1][shot] == 1 else '1'
        bitstrings.append(bit0 + bit1)
    
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
