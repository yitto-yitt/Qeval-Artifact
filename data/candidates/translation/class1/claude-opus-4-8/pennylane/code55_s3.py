# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def or_gate(a, b):
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    # 9 qubits: 0-2 = qr_a, 3-5 = qr_b, 6-8 = ancillary
    dev = qml.device("default.qubit", wires=9, shots=1024)

    @qml.qnode(dev)
    def circuit():
        # Initialize qr_a: flip if bit is '0' (active-low encoding matches Qiskit reference)
        for i in range(3):
            if a_bits[2 - i] == '0':
                qml.PauliX(wires=i)
        # Initialize qr_b
        for i in range(3):
            if b_bits[2 - i] == '0':
                qml.PauliX(wires=3 + i)
        # Toffoli gates: ancillary[i] = qr_a[i] AND qr_b[i]
        for i in range(3):
            qml.Toffoli(wires=[i, 3 + i, 6 + i])
        # Flip ancillary: NAND → OR
        for i in range(3):
            qml.PauliX(wires=6 + i)
        # Measure ancillary qubits (wires 6, 7, 8)
        return qml.sample(wires=[6, 7, 8])

    samples = circuit()

    counts = {}
    for sample in samples:
        # Convert bit array to string; wire 6 is MSB to match Qiskit bit ordering
        key = ''.join(str(int(b)) for b in sample)
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
