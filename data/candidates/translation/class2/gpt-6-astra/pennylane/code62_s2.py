# EVAL_META: task_id=62, framework=pennylane, class=2
import pennylane as qml


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    operations = [qml.Identity(wires=i) for i in range(num_qubits)]
    for i in range(len(basis)):
        if state[i] == 1:
            operations.append(qml.PauliX(wires=i))
        if basis[i] == 1:
            operations.append(qml.Hadamard(wires=i))
    return qml.tape.QuantumScript(operations)
