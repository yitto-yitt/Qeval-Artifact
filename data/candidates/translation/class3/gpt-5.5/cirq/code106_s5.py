# EVAL_META: task_id=106, framework=cirq, class=3
import cirq


def compose_cnot_dihedral():
    qubits = cirq.LineQubit.range(2)

    circ1 = cirq.Circuit()
    circ1.append(cirq.CNOT(qubits[0], qubits[1]))
    circ1.append(cirq.T(qubits[0]))

    circ2 = circ1.copy()
    circ2.append(cirq.X(qubits[1]), strategy=cirq.InsertStrategy.NEW)

    composed_circuit = circ1.copy()
    composed_circuit.append(circ2, strategy=cirq.InsertStrategy.NEW)
    return composed_circuit
