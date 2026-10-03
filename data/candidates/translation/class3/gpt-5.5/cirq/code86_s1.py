# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

def collect_linear_blocks_with_and_without_limit():
    q = cirq.LineQubit.range(5)

    full_linear_circuit = cirq.Circuit(
        cirq.CNOT(q[0], q[1]),
        cirq.CNOT(q[1], q[2]),
        cirq.CNOT(q[2], q[3]),
        cirq.CNOT(q[3], q[4]),
    )
    full_linear_gate = cirq.MatrixGate(
        full_linear_circuit.unitary(qubit_order=q)
    )

    full_block = cirq.Circuit(
        cirq.H(q[0]),
        full_linear_gate.on(*q),
    )

    first_limited_qubits = [q[0], q[1], q[2]]
    first_limited_circuit = cirq.Circuit(
        cirq.CNOT(q[0], q[1]),
        cirq.CNOT(q[1], q[2]),
    )
    first_limited_gate = cirq.MatrixGate(
        first_limited_circuit.unitary(qubit_order=first_limited_qubits)
    )

    second_limited_qubits = [q[2], q[3], q[4]]
    second_limited_circuit = cirq.Circuit(
        cirq.CNOT(q[2], q[3]),
        cirq.CNOT(q[3], q[4]),
    )
    second_limited_gate = cirq.MatrixGate(
        second_limited_circuit.unitary(qubit_order=second_limited_qubits)
    )

    limited_block = cirq.Circuit(
        cirq.H(q[0]),
        first_limited_gate.on(*first_limited_qubits),
        second_limited_gate.on(*second_limited_qubits),
    )

    return full_block, limited_block
