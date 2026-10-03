# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml

def noisy_bell():
    noise_strength = 0.05
    dev = qml.device("default.mixed", wires=2, shots=1000)
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(0)
        qml.CNOT(wires=[0, 1])
        qml.DepolarizingChannel(noise_strength, wires=0)
        qml.DepolarizingChannel(noise_strength, wires=1)
        return qml.counts(wires=[0, 1])
    counts = circuit()
    total = sum(counts.values())
    prob_dict = {}
    for key, value in counts.items():
        bitstring = ''.join(map(str, key))
        prob_dict[bitstring] = value / total
    return prob_dict
