# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml


def visualize_bell_states():
    device = qml.device("default.qubit", wires=2)

    @qml.set_shots(shots=1000)
    @qml.qnode(device)
    def circuit(minus):
        if minus:
            qml.PauliX(wires=0)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[1, 0])

    distributions = {}
    for name, minus in (("phi_plus", False), ("phi_minus", True)):
        counts = circuit(minus)
        total = sum(int(count) for count in counts.values())
        distributions[name] = {
            bitstring: int(count) / total for bitstring, count in counts.items()
        }
    return distributions
