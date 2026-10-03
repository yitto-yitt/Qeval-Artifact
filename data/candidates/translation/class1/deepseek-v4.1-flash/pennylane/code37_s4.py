# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml

def bv_algorithm(s):
    n = len(s)
    wires = n + 1
    ancilla = n
    dev = qml.device("default.qubit", wires=wires, shots=1)
    
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=ancilla)
        for i in range(wires):
            qml.Hadamard(wires=i)
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, ancilla])
        for i in range(n):
            qml.Hadamard(wires=i)
        return qml.sample(wires=list(range(n)))
    
    sample = circuit()
    bits = [str(int(sample[i, 0])) for i in range(n-1, -1, -1)]
    bitstring = ''.join(bits)
    bitstrings = [bitstring]
    return [bitstrings, sample]
