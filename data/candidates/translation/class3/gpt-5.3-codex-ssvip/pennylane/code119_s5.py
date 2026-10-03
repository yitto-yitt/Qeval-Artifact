# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in {"full", "half", "fixed"}:
        raise ValueError("kind must be one of {'full', 'half', 'fixed'}")

    if kind == "full":
        num_wires = 2 * num_state_qubits + 2
        c_in = 0
        a_start = 1
        b_start = 1 + num_state_qubits
        c_out = num_wires - 1
    elif kind == "half":
        num_wires = 2 * num_state_qubits + 2
        c_in = None
        a_start = 0
        b_start = num_state_qubits
        c_out = num_wires - 1
    else:  # fixed
        num_wires = 2 * num_state_qubits + 1
        c_in = None
        a_start = 0
        b_start = num_state_qubits
        c_out = None

    dev = qml.device("default.qubit", wires=num_wires)

    @qml.qnode(dev)
    def circuit():
        qml.CDKMAdder(
            wires=list(range(num_wires)),
            num_work_wires=num_state_qubits - 1,
            kind=kind,
        )
        return qml.state()

    return circuit
