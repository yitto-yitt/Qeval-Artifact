# EVAL_META: task_id=106, framework=cirq, class=3
import cirq


def compose_cnot_dihedral():
    qubits = cirq.LineQubit.range(2)
    circ1 = cirq.Circuit([cirq.CNOT(qubits[0], qubits[1]), cirq.T(qubits[0])])
    circ2 = cirq.Circuit([cirq.CNOT(qubits[0], qubits[1]), cirq.T(qubits[0]), cirq.X(qubits[1])])
    composed_circuit = cirq.Circuit(circ1, circ2)
    return composed_circuit
