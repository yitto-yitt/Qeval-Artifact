# EVAL_META: task_id=62, framework=cirq, class=2
import cirq


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()

    for i in range(len(basis)):
        if state[i] == 1:
            circuit.append(cirq.X(qubits[i]))
        if basis[i] == 1:
            circuit.append(cirq.H(qubits[i]))

    return circuit
