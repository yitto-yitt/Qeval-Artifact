# EVAL_META: task_id=62, framework=cirq, class=2
import cirq


def bb84_senders_circuit(state, basis):
    qubits = cirq.LineQubit.range(len(state))
    circuit = cirq.Circuit(cirq.I.on_each(*qubits))
    for i in range(len(basis)):
        if state[i] == 1:
            circuit.append(cirq.X(qubits[i]))
        if basis[i] == 1:
            circuit.append(cirq.H(qubits[i]))
    return circuit
