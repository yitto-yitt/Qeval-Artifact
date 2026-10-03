# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml

def and_gate(a, b):
    dev = qml.device("default.qubit", wires=9)

    @qml.qnode(dev)
    def circuit():
        a_bits = [(a >> i) & 1 for i in range(3)]
        b_bits = [(b >> i) & 1 for i in range(3)]
        initial_state = a_bits + b_bits + [0, 0, 0]
        qml.BasisState(initial_state, wires=range(9))
        qml.Toffoli(wires=[0, 3, 6])
        qml.Toffoli(wires=[1, 4, 7])
        qml.Toffoli(wires=[2, 5, 8])
        return qml.probs(wires=[8, 7, 6])

    probs = circuit()
    result = {}
    for i, p in enumerate(probs):
        if p > 1e-12:
            result[format(i, '03b')] = p
    return result
