# EVAL_META: task_id=117, framework=cirq, class=3
import cirq

def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    ops = cirq.two_qubit_matrix_to_operations(q0, q1, unitary, allow_partial_czs=False)
    circuit = cirq.Circuit()
    for op in ops:
        if isinstance(op.gate, cirq.CZPowGate) and op.gate.exponent == 1:
            a, b = op.qubits
            circuit.append([cirq.H(b), cirq.CNOT(a, b), cirq.H(b)])
        else:
            circuit.append(op)
    return circuit
