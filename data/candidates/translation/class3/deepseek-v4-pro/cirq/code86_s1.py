# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

def collect_linear_blocks_with_and_without_limit():
    q0, q1, q2, q3, q4 = cirq.LineQubit.range(5)

    # Full block (no width limit): entire circuit is one block
    a, b, c, d, e = [cirq.NamedQubit(name) for name in ['a', 'b', 'c', 'd', 'e']]
    sub_circ_full = cirq.Circuit([
        cirq.H(a),
        cirq.CX(a, b),
        cirq.CX(b, c),
        cirq.CX(c, d),
        cirq.CX(d, e)
    ])
    frozen_full = cirq.FrozenCircuit(sub_circ_full)
    op_full = cirq.CircuitOperation(frozen_full).on(q0, q1, q2, q3, q4)
    full_block = cirq.Circuit(op_full)

    # Limited block (max_block_width=3): split into two blocks
    # Block 1: qubits 0,1,2 with H, CX(0,1), CX(1,2)
    a1, b1, c1 = [cirq.NamedQubit(name) for name in ['a', 'b', 'c']]
    sub_circ1 = cirq.Circuit([
        cirq.H(a1),
        cirq.CX(a1, b1),
        cirq.CX(b1, c1)
    ])
    frozen1 = cirq.FrozenCircuit(sub_circ1)
    op1 = cirq.CircuitOperation(frozen1).on(q0, q1, q2)

    # Block 2: qubits 2,3,4 with CX(2,3), CX(3,4)
    b2, c2, d2 = [cirq.NamedQubit(name) for name in ['b', 'c', 'd']]
    sub_circ2 = cirq.Circuit([
        cirq.CX(b2, c2),
        cirq.CX(c2, d2)
    ])
    frozen2 = cirq.FrozenCircuit(sub_circ2)
    op2 = cirq.CircuitOperation(frozen2).on(q2, q3, q4)

    limited_block = cirq.Circuit(op1, op2)

    return full_block, limited_block
