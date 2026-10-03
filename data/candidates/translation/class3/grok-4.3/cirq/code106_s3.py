# EVAL_META: task_id=106, framework=cirq, class=3
import cirq


def compose_cnot_dihedral():
    qubits = cirq.LineQubit.range(2)
    circ1 = cirq.Circuit(cirq.CX(qubits[0], qubits[1]), cirq.T(qubits[0]))
    circ2 = circ1.copy()
    circ2.append(cirq.X(qubits[1]))
    composed_elem = circ2 + circ1
    return composed_elem
