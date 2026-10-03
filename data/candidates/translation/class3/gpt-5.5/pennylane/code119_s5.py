# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == "full":
        num_qubits = 2 * num_state_qubits + 2
    elif kind in ("half", "fixed"):
        num_qubits = 2 * num_state_qubits + 1
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    op = qml.CDKMRippleCarryAdder(wires=range(num_qubits), kind=kind)
    return qml.tape.QuantumScript([op])
