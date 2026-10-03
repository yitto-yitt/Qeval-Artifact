# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == "full":
        total_qubits = 2 * num_state_qubits + 2
    else:
        total_qubits = 2 * num_state_qubits + 1
    wires = list(range(total_qubits))
    dev = qml.device("default.qubit", wires=wires)

    @qml.qnode(dev)
    def circuit():
        # CDKM ripple-carry adder decomposition (simplified port of structure)
        for i in range(num_state_qubits):
            qml.Toffoli(wires=[i, num_state_qubits + i, total_qubits - 1])
            qml.CNOT(wires=[i, num_state_qubits + i])
            if i < num_state_qubits - 1 or kind == "full":
                qml.Toffoli(wires=[num_state_qubits + i, total_qubits - 1, i + 1])
        for i in range(num_state_qubits - 1, -1, -1):
            if i < num_state_qubits - 1 or kind == "full":
                qml.Toffoli(wires=[num_state_qubits + i, total_qubits - 1, i + 1])
            qml.CNOT(wires=[i, num_state_qubits + i])
            qml.Toffoli(wires=[i, num_state_qubits + i, total_qubits - 1])
        return qml.state()

    return circuit
