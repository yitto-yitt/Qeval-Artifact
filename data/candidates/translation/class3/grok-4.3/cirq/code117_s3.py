# EVAL_META: task_id=117, framework=cirq, class=3
import cirq

def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    cz_ops = cirq.two_qubit_matrix_to_cz_operations(q0, q1, unitary, allow_partial_czs=False)
    cz_circuit = cirq.Circuit(cz_ops)
    cnot_circuit = cirq.Circuit()
    for op in cz_circuit.all_operations():
        if isinstance(op.gate, cirq.CZPowGate):
            control, target = op.qubits
            cnot_circuit.append(cirq.H(target))
            cnot_circuit.append(cirq.CNOT(control, target))
            cnot_circuit.append(cirq.H(target))
        else:
            cnot_circuit.append(op)
    return cnot_circuit
