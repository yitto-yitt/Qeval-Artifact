# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml

def bv_algorithm(s):
    n = len(s)
    wires = list(range(n + 1))
    dev = qml.device("default.qubit", wires=wires, shots=1)
    
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n)
        for w in wires:
            qml.Hadamard(wires=w)
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, n])
        for w in range(n):
            qml.Hadamard(wires=w)
        return qml.sample(wires=range(n))
    
    result = circuit()
    sample = result[0]
    bitstring = ''.join(str(b) for b in reversed(sample))
    bitstrings = [bitstring]
    return [bitstrings, result]
