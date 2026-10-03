# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def bv_algorithm(s):
    n = len(s)
    dev = qml.device("default.qubit", wires=n+1, shots=1)

    @qml.qnode(dev)
    def circuit():
        # Ancilla is wire n
        qml.PauliX(wires=n)
        qml.Hadamard(wires=range(n+1))
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, n])
        qml.Hadamard(wires=range(n))
        # Measure input register in order from highest to lowest index
        return qml.sample(wires=range(n-1, -1, -1))

    result = circuit()
    bitstrings = []
    for sample in result:
        bitstring = ''.join(str(int(bit)) for bit in sample)
        bitstrings.append(bitstring)
    return [bitstrings, result]
