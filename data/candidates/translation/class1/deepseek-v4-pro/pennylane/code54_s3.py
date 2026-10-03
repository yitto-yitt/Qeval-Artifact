# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml

def and_gate(a, b):
    dev = qml.device("default.qubit", wires=9)

    a_bin = format(a, "03b")
    b_bin = format(b, "03b")

    @qml.qnode(dev)
    def circuit():
        # Encode a on wires 0,1,2 (LSB first)
        for i in range(3):
            if a_bin[2 - i] == "1":
                qml.PauliX(wires=i)

        # Encode b on wires 3,4,5 (LSB first)
        for i in range(3):
            if b_bin[2 - i] == "1":
                qml.PauliX(wires=3 + i)

        # Bitwise AND via Toffoli gates into ancillary wires 6,7,8
        for i in range(3):
            qml.Toffoli(wires=[i, 3 + i, 6 + i])

        # Measure each output bit separately to avoid bit-order ambiguity
        return qml.probs(wires=6), qml.probs(wires=7), qml.probs(wires=8)

    p0, p1, p2 = circuit()

    def bit_from_prob(prob):
        return 0 if prob[0] > prob[1] else 1

    result = f"{bit_from_prob(p2)}{bit_from_prob(p1)}{bit_from_prob(p0)}"
    return {result: 1.0}
