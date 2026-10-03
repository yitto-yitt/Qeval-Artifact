# EVAL_META: task_id=90, framework=cirq, class=3
import cirq


def create_custom_controlled():
    q0, q1, q2, q3 = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    circuit.append(cirq.X(q1).controlled_by(q0, q3))
    circuit.append(cirq.H(q2).controlled_by(q0, q3))
    return circuit
