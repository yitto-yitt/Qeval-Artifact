# EVAL_META: task_id=106, framework=cirq, class=3
import cirq


def compose_cnot_dihedral():
    q0, q1 = cirq.LineQubit.range(2)

    circ1 = cirq.Circuit(
        cirq.CNOT(q0, q1),
        cirq.T(q0),
    )
    circ2 = cirq.Circuit(circ1)
    circ2.append(cirq.X(q1))

    unitary1 = cirq.unitary(circ1)
    unitary2 = cirq.unitary(circ2)
    composed_unitary = unitary2 @ unitary1

    return cirq.MatrixGate(composed_unitary)
