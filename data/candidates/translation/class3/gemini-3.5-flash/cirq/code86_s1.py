# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    q0, q1, q2, q3, q4 = qubits

    # Circuit 1: No block width restriction (all CXs in one block)
    subcircuit1 = cirq.Circuit(
        cirq.CX(q0, q1),
        cirq.CX(q1, q2),
        cirq.CX(q2, q3),
        cirq.CX(q3, q4)
    )
    block1 = cirq.CircuitOperation(subcircuit1.freeze())
    circuit1 = cirq.Circuit(
        cirq.H(q0),
        block1
    )

    # Circuit 2: max_block_width of 3
    subcircuit2_1 = cirq.Circuit(
        cirq.CX(q0, q1),
        cirq.CX(q1, q2)
    )
    block2_1 = cirq.CircuitOperation(subcircuit2_1.freeze())

    subcircuit2_2 = cirq.Circuit(
        cirq.CX(q2, q3),
        cirq.CX(q3, q4)
    )
    block2_2 = cirq.CircuitOperation(subcircuit2_2.freeze())

    circuit2 = cirq.Circuit(
        cirq.H(q0),
        block2_1,
        block2_2
    )

    return circuit1, circuit2
