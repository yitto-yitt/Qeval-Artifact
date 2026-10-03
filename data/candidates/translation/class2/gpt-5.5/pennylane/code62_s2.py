# EVAL_META: task_id=62, framework=pennylane, class=2
import pennylane as qml


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    ops = []
    with qml.QueuingManager.stop_recording():
        for i in range(len(basis)):
            if state[i] == 1:
                ops.append(qml.PauliX(wires=i))
            if basis[i] == 1:
                ops.append(qml.Hadamard(wires=i))
    return qml.tape.QuantumScript(ops=ops, measurements=[])
