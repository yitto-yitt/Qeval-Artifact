# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml

def or_gate(a, b):
    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    dev = qml.device("default.qubit", wires=9, shots=1024)

    @qml.qnode(dev)
    def circuit():
        # qr_a: wires 0,1,2 ; qr_b: wires 3,4,5 ; ancillary: wires 6,7,8
        for i in range(3):
            if a_bits[2 - i] == "0":
                qml.PauliX(wires=i)
            if b_bits[2 - i] == "0":
                qml.PauliX(wires=3 + i)

        for i in range(3):
            qml.Toffoli(wires=[i, 3 + i, 6 + i])

        for i in range(3):
            qml.PauliX(wires=6 + i)

        return qml.sample(wires=[6, 7, 8])

    samples = circuit()
    counts = {}
    for s in samples:
        key = "".join(str(int(bit)) for bit in s)
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
