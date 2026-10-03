# EVAL_META: task_id=117, framework=cirq, class=3
import cirq

def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    ops = cirq.two_qubit_matrix_to_cz_operations(q0, q1, unitary)
    circuit = cirq.Circuit()

    for op in ops:
        if isinstance(op.gate, cirq.CZPowGate):
            target = op.qubits[1]
            circuit.append(cirq.H(target))
            circuit.append(cirq.CNOT(*op.qubits))
            circuit.append(cirq.H(target))
        else:
            circuit.append(op)

    return circuit
