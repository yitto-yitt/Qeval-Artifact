# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    num_wires = 2 * num_state_qubits + (1 if kind == "full" else 0)
    dev = qml.device("default.qubit", wires=num_wires)

    @qml.qnode(dev)
    def circuit():
        qml.CDKMRippleCarryAdder(num_state_qubits, kind, wires=range(num_wires))
        return qml.state()

    return circuit
