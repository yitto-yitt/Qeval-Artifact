# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in {"full", "half", "fixed"}:
        raise ValueError("kind must be one of 'full', 'half', or 'fixed'")

    if kind == "full":
        total_wires = 2 * num_state_qubits + 2
    elif kind == "half":
        total_wires = 2 * num_state_qubits + 1
    else:  # fixed
        total_wires = 2 * num_state_qubits

    dev = qml.device("default.qubit", wires=total_wires)

    @qml.qnode(dev)
    def circuit():
        qml.CDKMRippleCarryAdder(
            wires=list(range(total_wires)),
            kind=kind,
            mod=None if kind in {"full", "half"} else 2**num_state_qubits,
        )
        return qml.state()

    return circuit
