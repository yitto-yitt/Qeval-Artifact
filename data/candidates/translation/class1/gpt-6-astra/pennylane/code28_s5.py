# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml

def visualize_bell_states():
    dev = qml.device("default.qubit", wires=2)

    @qml.set_shots(shots=1000)
    @qml.qnode(dev)
    def bell_counts(minus):
        if minus:
            qml.PauliX(wires=0)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[1, 0])

    distributions = {}
    for name, minus in (("phi_plus", False), ("phi_minus", True)):
        counts = bell_counts(minus)
        total = sum(int(value) for value in counts.values())
        distributions[name] = {
            key: int(value) / total for key, value in counts.items()
        }
    return distributions
