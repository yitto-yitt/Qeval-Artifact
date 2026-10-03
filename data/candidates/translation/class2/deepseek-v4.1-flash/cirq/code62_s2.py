# EVAL_META: task_id=62, framework=cirq, class=2
import cirq


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    qubits = cirq.LineQubit.range(num_qubits)
    operations = []
    for i in range(len(basis)):
        if state[i] == 1:
            operations.append(cirq.X(qubits[i]))
        if basis[i] == 1:
            operations.append(cirq.H(qubits[i]))
    return cirq.Circuit(operations)
