# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    unitary = np.array(unitary, dtype=np.complex128)
    ops = cirq.two_qubit_matrix_to_cz_operations(q0, q1, unitary, allow_partial_czs=False)
    circuit = cirq.Circuit()
    for op in ops:
        if isinstance(op.gate, cirq.CZPowGate):
            circuit.append(cirq.H(q1))
            circuit.append(cirq.CNOT(q0, q1))
            circuit.append(cirq.H(q1))
        else:
            circuit.append(op)
    return circuit
