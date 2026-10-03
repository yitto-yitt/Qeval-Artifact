# EVAL_META: task_id=86, framework=cirq, class=3
import cirq


def collect_linear_blocks_with_and_without_limit():
    q = cirq.LineQubit.range(5)
    circuit = cirq.Circuit(
        cirq.H(q[0]),
        cirq.CNOT(q[0], q[1]),
        cirq.CNOT(q[1], q[2]),
        cirq.CNOT(q[2], q[3]),
        cirq.CNOT(q[3], q[4]),
    )
    full_block = circuit.copy()
    limited_block = circuit.copy()
    return full_block, limited_block
