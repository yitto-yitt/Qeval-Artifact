# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append([cirq.I(q0), cirq.I(q1)])

    ops = cirq.two_qubit_matrix_to_cz_operations(
        q0, q1, np.asarray(unitary), allow_partial_czs=False
    )

    for op in ops:
        if isinstance(op.gate, cirq.CZPowGate) and np.isclose(abs(op.gate.exponent), 1):
            a, b = op.qubits
            circuit.append([cirq.H(b), cirq.CX(a, b), cirq.H(b)])
        else:
            circuit.append(op)

    return circuit
