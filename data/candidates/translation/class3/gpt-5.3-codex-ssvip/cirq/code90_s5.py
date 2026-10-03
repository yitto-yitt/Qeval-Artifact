# EVAL_META: task_id=90, framework=cirq, class=3
import cirq


def create_custom_controlled():
    q = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    op = cirq.X(q[1]).controlled_by(q[0], q[3])
    op2 = cirq.H(q[2]).controlled_by(q[0], q[3])
    circuit.append([op, op2])
    return circuit
