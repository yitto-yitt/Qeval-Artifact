# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def noisy_bell():
    dev = qml.device("default.mixed", wires=2, shots=1000)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        # Approximate noise from FakeBelemV2
        qml.DepolarizingChannel(0.01, wires=0)
        qml.DepolarizingChannel(0.01, wires=1)
        qml.BitFlip(0.02, wires=0)
        qml.BitFlip(0.02, wires=1)
        return qml.probs(wires=[0, 1])
    
    probs = circuit()
    result = {}
    for i, p in enumerate(probs):
        # PennyLane index i: wire 0 is most significant bit
        # Qiskit bitstring: wire 1 is most significant bit (little-endian)
        bitstring = format(i, '02b')[::-1]
        result[bitstring] = float(p)
    return result
