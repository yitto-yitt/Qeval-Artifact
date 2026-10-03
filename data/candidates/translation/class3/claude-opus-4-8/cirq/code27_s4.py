# EVAL_META: task_id=27, framework=cirq, class=3
import cirq


def apply_op_back():
    qubits = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CX(qubits[0], qubits[1]))
    circuit.append(cirq.H(qubits[0]))
    return circuit
