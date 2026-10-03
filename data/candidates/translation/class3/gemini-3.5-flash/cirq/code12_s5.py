# EVAL_META: task_id=12, framework=cirq, class=3
import cirq


def get_unitary():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.H(qubits[0]), cirq.CNOT(qubits[0], qubits[1]))
    return cirq.unitary(circuit, qubit_order=[qubits[1], qubits[0]])
