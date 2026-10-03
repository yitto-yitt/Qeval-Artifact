# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml

def bv_algorithm(s):
    n = len(s)
    dev = qml.device("default.qubit", wires=n + 1, shots=1)

    @qml.qnode(dev)
    def circuit():
        ancilla = n
        qml.PauliX(wires=ancilla)
        for w in range(n + 1):
            qml.Hadamard(wires=w)
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, ancilla])
        for i in range(n):
            qml.Hadamard(wires=i)
        return qml.sample(wires=range(n))

    sample_result = circuit()
    bitstring = "".join(str(int(bit)) for bit in sample_result[::-1])
    bitstrings = [bitstring]
    result = sample_result
    return [bitstrings, result]
