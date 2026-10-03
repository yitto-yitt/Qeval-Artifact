# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml

def visualize_bell_states():
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def phi_plus_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1])

    @qml.qnode(dev)
    def phi_minus_circuit():
        qml.PauliX(wires=0)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1])

    def to_bitstring_dict(probs):
        dist = {}
        for idx, p in enumerate(probs):
            if p > 1e-12:
                dist[format(idx, "02b")] = float(p)
        return dist

    return {
        "phi_plus": to_bitstring_dict(phi_plus_circuit()),
        "phi_minus": to_bitstring_dict(phi_minus_circuit()),
    }
