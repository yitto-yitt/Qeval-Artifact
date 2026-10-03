# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == "full":
        num_qubits = 2 * num_state_qubits + 2
    elif kind in ("half", "fixed"):
        num_qubits = 2 * num_state_qubits + 1
    else:
        num_qubits = 2 * num_state_qubits + 2

    dev = qml.device("default.qubit", wires=num_qubits)

    def maj(a, b, c):
        qml.CNOT(wires=[b, a])
        qml.CNOT(wires=[b, c])
        qml.Toffoli(wires=[a, c, b])

    def uma(a, b, c):
        qml.Toffoli(wires=[a, c, b])
        qml.CNOT(wires=[b, c])
        qml.CNOT(wires=[b, a])

    @qml.qnode(dev)
    def circuit():
        if kind == "full":
            carry_in = num_state_qubits * 2
            for i in range(num_state_qubits):
                maj(i, num_state_qubits + i, carry_in if i == 0 else carry_in + i)
            for i in range(num_state_qubits - 1, -1, -1):
                uma(i, num_state_qubits + i, carry_in if i == 0 else carry_in + i)
        elif kind == "half":
            for i in range(num_state_qubits):
                maj(i, num_state_qubits + i, num_state_qubits * 2 if i == 0 else num_state_qubits * 2 + i - 1)
            for i in range(num_state_qubits - 1, -1, -1):
                uma(i, num_state_qubits + i, num_state_qubits * 2 if i == 0 else num_state_qubits * 2 + i - 1)
        else:
            for i in range(num_state_qubits):
                maj(i, num_state_qubits + i, num_state_qubits * 2 if i == 0 else num_state_qubits * 2 + i - 1)
            for i in range(num_state_qubits - 1, -1, -1):
                uma(i, num_state_qubits + i, num_state_qubits * 2 if i == 0 else num_state_qubits * 2 + i - 1)
        return qml.state()

    return circuit
