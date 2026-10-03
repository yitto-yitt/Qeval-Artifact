# EVAL_META: task_id=117, framework=cirq, class=3
import cirq

def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    ops = cirq.two_qubit_matrix_to_cz_operations(q0, q1, unitary)
    circuit = cirq.Circuit(ops)
    new_circuit = cirq.Circuit()
    for moment in circuit:
        for op in moment:
            if isinstance(op.gate, cirq.CZPowGate) and op.gate.exponent % 2 == 1:
                control, target = op.qubits
                new_circuit.append([cirq.H(target), cirq.CNOT(control, target), cirq.H(target)])
            else:
                new_circuit.append(op)
    return new_circuit
